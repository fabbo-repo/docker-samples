import os
import sys
import subprocess
from key_check import (
    get_api_key
)
from key_generator import (
    create_api_key,
    create_auth_key
)

TAILSCALE_ENV_PATH = "tailscale.env"
TAILSCALE_SCRIPT_ENV_PATH = "tailscale_script.env"

env_variables = {}


def main():
    """
    MAIN method
    """

    if not os.path.exists(TAILSCALE_SCRIPT_ENV_PATH):
        print(f"Missing env variables file: {TAILSCALE_SCRIPT_ENV_PATH}")
        sys.exit(-2)

    with open(TAILSCALE_SCRIPT_ENV_PATH, "r", encoding="utf8") as file:
        for line in file.read().splitlines():
            env_values = line.split("=")
            env_variables[env_values[0]] = "=".join(env_values[1:])

    (
        tailscale_client_id,
        tailscale_client_secret,
        tailscale_tailnet,
        tailscale_tag
    ) = check_env(env_variables)

    ts_api_key = get_api_key(
        tailscale_client_id,
        tailscale_client_secret
    )

    if not ts_api_key:
        print("Unable to authenticate")
        sys.exit(-1)

    tailscale_auth_id = env_variables.get("TS_AUTH_ID")

    if tailscale_auth_id:
        print("Creating new API Key...")
        create_and_replace_auth_key(
            tailscale_client_id,
            tailscale_client_secret,
            tailscale_tailnet,
            tailscale_tag
        )
    else:
        create_and_replace_auth_key(
            tailscale_client_id,
            tailscale_client_secret,
            tailscale_tailnet,
            tailscale_tag
        )


def create_and_replace_auth_key(
    tailscale_client_id,
    tailscale_client_secret,
    tailscale_tailnet,
    tailscale_tag
):

    ts_api_key = create_api_key(
        tailscale_client_id,
        tailscale_client_secret
    )

    if ts_api_key:
        ts_auth_id, ts_auth_key = create_auth_key(
            ts_api_key,
            tailscale_tailnet,
            tailscale_tag
        )

        with open(TAILSCALE_SCRIPT_ENV_PATH, "w", encoding="utf8") as file:
            env_variables["TS_AUTH_ID"] = ts_auth_id
            env_file_content = ""
            for env_key in list(env_variables.keys()):
                env_file_content += f"{env_key}={env_variables[env_key]}\n"
            file.write(env_file_content)

        print("Reading service env file")
        service_env_variables = {}
        with open(TAILSCALE_ENV_PATH, "r", encoding="utf8") as file:
            for line in file.read().splitlines():
                env_values = line.split("=")
                service_env_variables[env_values[0]] = "=".join(env_values[1:])
        print("Overriding service env file")
        with open(TAILSCALE_ENV_PATH, "w", encoding="utf8") as file:
            service_env_variables["TS_AUTHKEY"] = ts_auth_key
            env_file_content = ""
            for env_key in list(service_env_variables.keys()):
                env_file_content += f"{env_key}={service_env_variables[env_key]}\n"
            file.write(env_file_content)

        print("New env file")

        print("Stopping service")
        subprocess.run(["docker", "compose", "down"], check=False)

        print("Launching service")
        subprocess.run(["docker", "compose", "up", "-d"], check=False)

        print("Task finished")


def check_env(env_variables: dict):
    # Get OAuth client variables
    tailscale_client_id = env_variables.get("TS_OAUTH_CLIENT_ID")
    if not tailscale_client_id:
        print("Missing TS_OAUTH_CLIENT_ID")
        sys.exit(-5)
    tailscale_client_secret = env_variables.get("TS_OAUTH_CLIENT_SECRET")
    if not tailscale_client_secret:
        print("Missing TS_OAUTH_CLIENT_SECRET")
        sys.exit(-5)
    # Get tailscale data variables
    tailscale_tailnet = env_variables.get("TS_TAILNET")
    if not tailscale_tailnet:
        print("Missing TS_TAILNET")
        sys.exit(-5)
    tailscale_tag = env_variables.get("TS_TAG")
    if not tailscale_tag:
        print("Missing TS_TAG")
        sys.exit(-5)
    return (
        tailscale_client_id,
        tailscale_client_secret,
        tailscale_tailnet,
        tailscale_tag
    )


if __name__ == "__main__":
    main()
