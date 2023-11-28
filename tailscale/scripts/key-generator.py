import os
import requests
import json

"""
[Docs](https://github.com/tailscale/tailscale/blob/main/api.md)
"""


def get_api_key(
        tailscale_client_id: str,
        tailscale_client_secret: str
) -> str | None:
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
        return None


def get_auth_key(
        ts_api_key: str,
        tailscale_tailnet: str,
        tailscale_tag: str
) -> tuple | None:
    ts_auth_url = f"https://api.tailscale.com/api/v2/tailnet/{tailscale_tailnet}/keys"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ts_api_key}"
    }
    data = {
        "capabilities": {
            "devices": {
                "create": {
                    "reusable": True,
                    "ephemeral": True,
                    "tags": [f"tag:{tailscale_tag}"]
                }
            }
        },
        "expirySeconds": 7776000,
        "description": f"VPN {tailscale_tag}"
    }

    # Request auth key
    response = requests.post(
        ts_auth_url,
        headers=headers,
        data=json.dumps(data)
    )

    if response.status_code == 200:
        return (response.json()["id"], response.json()["key"])
    else:
        print(
            f"Error requesting Auth key. Status code: {response.status_code}")
        print(response.text)
        return None


def main():
    """
    MAIN method
    """
    # Get OAuth client variables
    tailscale_client_id = os.environ.get("TS_OAUTH_CLIENT_ID")
    if not tailscale_client_id:
        print("Missing TS_OAUTH_CLIENT_ID")
        return
    tailscale_client_secret = os.environ.get("TS_OAUTH_CLIENT_SECRET")
    if not tailscale_client_secret:
        print("Missing TS_OAUTH_CLIENT_SECRET")
        return
    # Get tailscale data variables
    tailscale_tailnet = os.environ.get("TS_TAILNET")
    if not tailscale_tailnet:
        print("Missing TS_TAILNET")
        return
    tailscale_tag = os.environ.get("TS_TAG")
    if not tailscale_tag:
        print("Missing TS_TAG")
        return

    ts_api_key = get_api_key(
        tailscale_client_id,
        tailscale_client_secret
    )

    if ts_api_key:
        ts_auth_id, ts_auth_key = get_auth_key(
            ts_api_key,
            tailscale_tailnet,
            tailscale_tag
        )
        print(ts_auth_id)
        print(ts_auth_key)


if __name__ == "__main__":
    main()
