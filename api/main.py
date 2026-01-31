from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import datetime, timedelta
from pydantic import BaseModel
from src.auth_db import authenticate, create_user, update_credentials, init_db
import os

SECRET_KEY = os.getenv("SECRET_KEY", "DEV_SECRET_KEY_CHANGE_ME")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

app = FastAPI(title="DataCo Supply Chain API")

# ✅ INIT DB AU DÉMARRAGE
init_db()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ------------------ SCHEMAS ------------------
class CreateUserRequest(BaseModel):
    first_name: str | None = None
    last_name: str
    username: str
    email: str
    password: str
    role: str


class UpdateCredentialsRequest(BaseModel):
    user_id: int
    new_username: str
    new_password: str


# ------------------ ROUTES ------------------
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(
        {"sub": user["username"], "role": user["role"], "id": user["id"]},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"access_token": token, "token_type": "bearer"}


@app.post("/create_user")
def create_user_api(
    data: CreateUserRequest,
    current_user=Depends(get_current_user)
):
    if current_user["role"] != "patron":
        raise HTTPException(status_code=403, detail="Not allowed")

    create_user(
        data.first_name,
        data.last_name,
        data.username,
        data.email,
        data.password,
        data.role
    )
    return {"status": "ok", "message": "User created"}


@app.put("/update_credentials")
def update_credentials_api(
    data: UpdateCredentialsRequest,
    current_user=Depends(get_current_user)
):
    if current_user["id"] != data.user_id:
        raise HTTPException(status_code=403, detail="Not allowed")

    update_credentials(
        data.user_id,
        data.new_username,
        data.new_password
    )
    return {"status": "ok", "message": "Credentials updated"}

# ------------------ NOUVEL ENDPOINT ------------------
@app.get("/me")
def me(current_user: dict = Depends(get_current_user)):
    """
    Récupère les infos complètes de l'utilisateur connecté via le token JWT.
    """
    from src.auth_db import get_user_by_id

    user = get_user_by_id(current_user["id"])
    if not user:
        raise HTTPException(status_code=404, detail="Cannot fetch user info")
    
    return user
