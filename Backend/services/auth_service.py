import jwt
import datetime
from config import JWT_SECRET, JWT_ALGORITHM, JWT_EXP_MINUTES


ADMIN_USER = {"username": "admin", "password": "12345"}

def authenticate(username, password):
    if username == ADMIN_USER["username"] and password == ADMIN_USER["password"]:
        payload = {
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=JWT_EXP_MINUTES)
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token
    return None

def verify_token(token):
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
