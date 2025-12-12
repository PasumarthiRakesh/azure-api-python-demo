from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
import datetime

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "MY_SECRET_KEY_DEMO"
ALGORITHM = "HS256"


@app.post("/token")
def generate_token():
    payload = {
        "user": "demo_user",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token}


@app.get("/secure-data")
def secure_data(token: str = Depends(oauth2_scheme)):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {"message": "Secure API access successful!"}
    except:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
