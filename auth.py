import os
import json
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


def init_firebase():
    """Initialize Firebase Admin, preferring a local file then env JSON."""
    if firebase_admin._apps:
        return 

    file_path = "serviceAccountKey.json"
    env_json = os.getenv("FIREBASE_CREDENTIALS")

    service_account_info = None

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as cred_file:
            service_account_info = json.load(cred_file)
    elif env_json:
        try:
            service_account_info = json.loads(env_json)
        except json.JSONDecodeError as exc:
            raise RuntimeError("FIREBASE_CREDENTIALS contains invalid JSON") from exc

    if service_account_info is None:
        raise RuntimeError(
            "Firebase credentials not found. Provide serviceAccountKey.json or set FIREBASE_CREDENTIALS."
        )

    cred = credentials.Certificate(service_account_info)
    firebase_admin.initialize_app(cred)


security = HTTPBearer(auto_error=False)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Missing bearer token")

    token = credentials.credentials
    try:
        decoded = firebase_auth.verify_id_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired Firebase ID token")

    return decoded 