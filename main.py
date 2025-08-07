from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

app = FastAPI()

# Dummy user database
fake_user_db = {
    "sumaiah": {
        "username": "sumaiah",
        "password": "summi",  # static password
    }
}

# JWT config
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Authenticate user (static password logic)
def authenticate_user(username: str, password: str):
    user = fake_user_db.get(username)
    if not user or password != "summi":
        return False
    return user

# JWT token creation
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Login route
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

# Dependency to get current user
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None or username not in fake_user_db:
            raise HTTPException(status_code=401, detail="Invalid token")
        return fake_user_db[username]
    except JWTError:
        raise HTTPException(status_code=401, detail="Token verification failed")

# Protected route
@app.get("/profile")
def read_profile(current_user: dict = Depends(get_current_user)):
    return {"message": f"Hello, {current_user['username']}! Welcome to your profile."}