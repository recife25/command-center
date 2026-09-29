# import json
# import msal

# def load_config():
#     with open("config/msal_config.json") as f:
#         return json.load(f)

# def get_token():
#     config = load_config()

#     app = msal.PublicClientApplication(
#         client_id=config["client_id"],
#         authority=config["authority"]
#     )

#     result = app.acquire_token_interactive(
#         scopes=config["scopes"],
#         use_default_redirect_uri=True
#     )

#     if "access_token" not in result:
#         raise Exception("Authentication failed")

#     return result["access_token"]
#We're unable to complete your request

#invalid_request: The provided value for the input parameter 'redirect_uri' is not valid. The expected value is a URI which matches a redirect URI registered for #this client application.


# import json
# import msal

# def load_config():
#     with open("config/msal_config.json") as f:
#         return json.load(f)

# def get_token():
#     config = load_config()

#     app = msal.PublicClientApplication( 
#         client_id=config["client_id"],
#         authority=config["authority"]
#     )

#     result = app.acquire_token_interactive(
#         scopes=config["scopes"],
#         open_browser=True
#     )

#     if "access_token" not in result:
#         raise Exception("Authentication failed")

#     return result["access_token"]
#MSAL is authenticating, but your Python script is NOT receiving the token. python graph requests will fail without a valid access token.

# import json
# import msal

# def load_config():
#     with open("config/msal_config.json") as f:
#         return json.load(f)

# def get_token():
#     config = load_config()

#     app = msal.PublicClientApplication(
#         client_id=config["client_id"],
#         authority=config["authority"]
#     )

#     flow = app.initiate_device_flow(scopes=config["scopes"])
#     if "user_code" not in flow:
#         raise Exception("Failed to create device flow")

#     print("Go to:", flow["verification_uri"])
#     print("Enter code:", flow["user_code"])

#     result = app.acquire_token_by_device_flow(flow)

#     if "access_token" not in result:
#         raise Exception("Authentication failed")

#     return result["access_token"]


# import msal
# import json
# import os

# CLIENT_ID = "<YOUR_CLIENT_ID>"
# TENANT = "consumers"
# AUTHORITY = f"https://login.microsoftonline.com/{TENANT}"
# SCOPES = ["User.Read", "Mail.Send", "Calendars.ReadWrite", "offline_access"]

# TOKEN_PATH = "token.json"

# def load_token():
#     if os.path.exists(TOKEN_PATH):
#         with open(TOKEN_PATH, "r") as f:
#             return json.load(f)
#     return None

# def save_token(token):
#     with open(TOKEN_PATH, "w") as f:
#         json.dump(token, f)

# def get_token():
#     token = load_token()

#     app = msal.PublicClientApplication(
#         CLIENT_ID,
#         authority=AUTHORITY
#     )

#     # Try refresh token first
#     if token and "refresh_token" in token:
#         result = app.acquire_token_by_refresh_token(
#             token["refresh_token"],
#             scopes=SCOPES
#         )
#         if "access_token" in result:
#             save_token(result)
#             return result["access_token"]

#     # Device code flow (interactive login)
#     flow = app.initiate_device_flow(scopes=SCOPES)
#     if "user_code" not in flow:
#         raise Exception("Failed to create device flow")

#     print(f"Go to {flow['verification_uri']} and enter code: {flow['user_code']}")

#     result = app.acquire_token_by_device_flow(flow)

#     if "access_token" in result:
#         save_token(result)
#         return result["access_token"]

#     raise Exception("Authentication failed")

import msal
import json
import os

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

CLIENT_ID = "f3ad4717-d95a-4ded-8e94-9a2a4160cf0d" # Replace with your Azure App Registration client ID
# #TENANT = "consumers"             # Personal Microsoft accounts use the 'consumers' tenant
# AUTHORITY = f"https://login.microsoftonline.com/{TENANT}"
#AUTHORITY = "https://login.microsoftonline.com/common"
AUTHORITY = "https://login.microsoftonline.com/consumers"



# PERSONAL ACCOUNT SAFE SCOPES — DO NOT ADD offline_access, openid, profile
SCOPES = [
    "User.Read",
    "Mail.Send",
    "Calendars.ReadWrite"
]

TOKEN_PATH = "token.json"


# ---------------------------------------------------------
# TOKEN HELPERS
# ---------------------------------------------------------

def load_token():
    """Load token.json if it exists."""
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, "r") as f:
            return json.load(f)
    return None


def save_token(token):
    """Save token.json after authentication."""
    with open(TOKEN_PATH, "w") as f:
        json.dump(token, f)

# ---------------------------------------------------------
# MAIN AUTH FUNCTION
# ---------------------------------------------------------

def get_token():
    """Authenticate using MSAL Device Code Flow (personal Microsoft accounts)."""
    token = load_token()

    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority=AUTHORITY
    )

    # 1. Try cached access token first
    if token and "access_token" in token:
        print("\nLoaded cached token:")
        print(token)  # DEBUG
        return token["access_token"]

    # 2. Device code flow (ONLY supported method for personal accounts)
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        print("\nMSAL ERROR OBJECT:\n", flow, "\n")
        raise Exception("Failed to create device flow")

    print(f"\nGo to {flow['verification_uri']} and enter code: {flow['user_code']}\n")

    result = app.acquire_token_by_device_flow(flow)

    print("\nMSAL RESULT:\n", result, "\n")  # DEBUG

    # 3. Save token.json
    if "access_token" in result:
        save_token(result)
        return result["access_token"]

    raise Exception("Authentication failed")
