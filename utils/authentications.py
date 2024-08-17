import base64
from requests.auth import HTTPBasicAuth

def create_api_token_v1(email:str,api_token:str)  -> str:
    auth_token_v1 = base64.b64encode(f"{email}:{api_token}".encode()).decode('utf-8')
    return auth_token_v1


def create_api_token_v2(email:str,api_token:str)  -> HTTPBasicAuth:
    auth_token_v2 = HTTPBasicAuth(email,api_token)
    return auth_token_v2