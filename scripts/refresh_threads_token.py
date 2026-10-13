"""Refresh the Meta Threads token and replace its GitHub repository secret."""
import datetime as dt
import json
import os
import re
import subprocess
import urllib.error
import urllib.parse
import urllib.request


def refresh(token):
    query = urllib.parse.urlencode({"grant_type": "th_refresh_token", "access_token": token})
    request = urllib.request.Request("https://graph.threads.net/refresh_access_token?" + query)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.load(response)
    except urllib.error.HTTPError as exc:
        try:
            data = json.loads(exc.read())
            error = data.get("error", data)
            message = str(error.get("message") or error.get("error_message") or "No explanation provided")
            message = re.sub(r"https?://\S+", "[URL omitted]", message.replace(token, "[token omitted]"))
            code = error.get("code", "unknown")
        except (ValueError, AttributeError):
            message, code = "No structured explanation provided", "unknown"
        raise RuntimeError(f"Meta token refresh failed (HTTP {exc.code}, code {code}): {message[:400]}") from None
    except urllib.error.URLError:
        raise RuntimeError("Unable to reach Meta token refresh endpoint") from None
    renewed = result.get("access_token")
    lifetime = result.get("expires_in")
    if not isinstance(renewed, str) or not renewed.strip() or not isinstance(lifetime, int) or lifetime <= 0:
        raise RuntimeError("Meta returned an invalid token refresh response")
    return renewed, lifetime


def main():
    token = os.environ.get("THREADS_ACCESS_TOKEN", "").strip()
    updater = os.environ.get("THREADS_SECRET_UPDATE_TOKEN", "").strip()
    repo = os.environ.get("GITHUB_REPOSITORY", "").strip()
    if not token or not updater or not repo:
        raise RuntimeError("Missing Threads token, secret update credential, or repository")
    # Check write access credentials before asking Meta to refresh the token.
    env = {**os.environ, "GH_TOKEN": updater}
    check = subprocess.run(["gh", "api", f"repos/{repo}/actions/secrets/public-key"], env=env, capture_output=True)
    if check.returncode:
        raise RuntimeError("Cannot access repository secrets; check the GitHub token permissions and expiration")
    renewed, lifetime = refresh(token)
    if os.environ.get("GITHUB_ACTIONS") == "true":
        print(f"::add-mask::{renewed}", flush=True)
    result = subprocess.run(["gh", "secret", "set", "THREADS_ACCESS_TOKEN", "--repo", repo], input=renewed.encode(), env=env, capture_output=True)
    if result.returncode:
        raise RuntimeError("Meta refreshed the token but GitHub secret update failed; retry the workflow immediately")
    expires = dt.datetime.now(dt.timezone.utc) + dt.timedelta(seconds=lifetime)
    print(f"Threads token refreshed and stored. Expiration: {expires.isoformat(timespec='seconds')}")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ValueError, OSError) as exc:
        # Never print raw HTTP bodies, request URLs, or subprocess output.
        raise SystemExit(f"Token renewal failed: {exc}") from None
