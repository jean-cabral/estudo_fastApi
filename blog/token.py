from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError


SECRET_KEY = "d3b1cd436551feb7bc2561ee13de2f3ee40cd14025f94dfd452ce0e4539842d4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt