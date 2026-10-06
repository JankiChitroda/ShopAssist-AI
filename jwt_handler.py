import jwt
from functools import wraps
from flask import request, redirect, url_for

SECRET_KEY = "supportpilot_secret_key"

def generate_token(full_name, email):
    payload = {
        "full_name": full_name,
        "email": email
    }
    # Encode the payload into a JWT token string
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Look for the auth_token cookie
        token = request.cookies.get("auth_token")
        if not token:
            return redirect(url_for("login"))
        try:
            # Try decoding the token to verify it's valid
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated