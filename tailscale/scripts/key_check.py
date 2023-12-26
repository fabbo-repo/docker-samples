import os
import datetime
import sys
import requests

# [Docs](https://github.com/tailscale/tailscale/blob/main/api.md)


def get_api_key(
        tailscale_client_id: str,
        tailscale_client_secret: str
) -> str:
    ts_auth_url = "https://api.tailscale.com/api/v2/oauth/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "client_id": tailscale_client_id,
        "client_secret": tailscale_client_secret,
        "grant_type": "client_credentials"
    }

    # Request api key
    response = requests.post(
        ts_auth_url,
        headers=headers,
        data=data
    )

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Error requesting API key. Status code: {response.status_code}")
        print(response.text)
        sys.exit(-1)


def str_to_datetime(dt_str):
    dt, _, _ = dt_str.partition(".")
    dt = datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%SZ")
    return dt


def is_expired_auth_key(
        ts_api_key: str,
        tailscale_auth_id: str,
        tailscale_tailnet: str
) -> str:
    ts_auth_url = f"https://api.tailscale.com/api/v2/tailnet/{tailscale_tailnet}/keys/{tailscale_auth_id}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ts_api_key}"
    }

    # Request auth key
    response = requests.get(
        ts_auth_url,
        headers=headers
    )

    if response.status_code == 200:
        return str_to_datetime(response.json()["expires"]) <= datetime.datetime.now()
    else:
        print(
            f"Error requesting Auth key data. Status code: {response.status_code}")
        print(response.text)
        sys.exit(-2)


def check_key_check_env():
    # Get OAuth client variables
    tailscale_client_id = os.environ.get("TS_OAUTH_CLIENT_ID")
    if not tailscale_client_id:
        print("Missing TS_OAUTH_CLIENT_ID")
        sys.exit(-5)
    tailscale_client_secret = os.environ.get("TS_OAUTH_CLIENT_SECRET")
    if not tailscale_client_secret:
        print("Missing TS_OAUTH_CLIENT_SECRET")
        sys.exit(-5)
    # Get tailscale data variables
    tailscale_tailnet = os.environ.get("TS_TAILNET")
    if not tailscale_tailnet:
        print("Missing TS_TAILNET")
        sys.exit(-5)
    tailscale_auth_id = os.environ.get("TS_AUTH_ID")
    if not tailscale_auth_id:
        print("Missing TS_AUTH_ID")
        sys.exit(-5)
    return (
        tailscale_client_id,
        tailscale_client_secret,
        tailscale_tailnet,
        tailscale_auth_id
    )


def main():
    """
    MAIN method
    """

    (
        tailscale_client_id,
        tailscale_client_secret,
        tailscale_tailnet,
        tailscale_auth_id
    ) = check_key_check_env()

    ts_api_key = get_api_key(
        tailscale_client_id,
        tailscale_client_secret
    )

    if ts_api_key:
        is_expired = is_expired_auth_key(
            ts_api_key,
            tailscale_auth_id,
            tailscale_tailnet
        )
        if is_expired:
            print("Key has expired")
            sys.exit(1)
        else:
            print("Key has not expired")
            sys.exit(0)


if __name__ == "__main__":
    main()
