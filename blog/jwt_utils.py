from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, status
import os

# Constants for JWT configuration (replace hardcoded values with environment variables)
SECRET_KEY = os.getenv("SECRET_KEY", "a_very_secret_key")  # Ensure to set this in your environment
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Function to create a JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Creates a JWT access token with the given data and expiration time.

    Args:
        data (dict): The payload to encode in the JWT token.
        expires_delta (timedelta, optional): Custom expiration time for the token.
            Defaults to ACCESS_TOKEN_EXPIRE_MINUTES.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Function to decode a JWT token and extract user information
def get_user_from_token(token: str):
    """
    Decodes a JWT token and extracts the user ID from the payload.

    Args:
        token (str): The JWT token to decode.

    Returns:
        int: The user ID extracted from the token.

    Raises:
        HTTPException: If the token is invalid or user ID is missing.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return user_id
    except JWTError:
        raise credentials_exception
