from fastapi import FastAPI, Body, Header
import database_utils as dbu
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
import base_models as bm


origins = [
    "http://localhost:4200",
    "http://localhost",
]

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "c8a7f2bcb3eae031d9ac9b6cf439ff85d32a86c1d26bc05ae8fe4a0b4697e35d"

# encryption algorithm
ALGORITHM = "HS256"


@app.get("/form/get_form_data")
async def get_form_data(auth: str = Header(...), form_id: str = Header(...)):
    if verify_token(auth) == -1:
        return {"error": "Unauthorized access"}
    return dbu.get_form(form_id)


@app.post("/form/create_form")
async def create_form(form_data: bm.FormCreation, auth: str = Header(...)):
    if verify_token(auth) == -1:
        return {"error": "Unauthorized access"}

    form_data = form_data.dict()
    form_id = dbu.create_form(form_data)
    form = dbu.get_form(form_id)
    message = {
        "message": "Created successfully!",
        "form_data": form
    }
    return message


@app.get("/form/get_form_submissions")
async def get_form_submissions(auth: str = Header(...), form_id: str = Header(...)):
    if verify_token(auth) == -1:
        return {"error": "Unauthorized access"}
    return dbu.get_form_submissions(form_id)


@app.put("/form/change_form_status")
async def change_form_status(status: bool = Header(...), auth: str = Header(...), form_id: str = Header(...)):
    if verify_token(auth) == -1:
        return {"error": "Unauthorized access"}
    dbu.change_form_status(form_id, status)


@app.post("/form/submit")
async def submit(data: bm.Submission, auth: str = Header(...)):
    if verify_token(auth) == -1:
        return {"error": "Unauthorized access"}

    data = data.dict()
    form_id = data['form_id']
    options = data['options']

    user_id = verify_token(auth)
    if dbu.create_submission(form_id, user_id['user_id'], options):
        return "Successful submission!"
    return "Unsuccessful submission!"


@app.get("/form/check_form_completed")
async def check_form_completed(form_id: str = Header(...), auth: str = Header(...)):
    if verify_token(auth) == -1:
        return {"error": "Unauthorized access"}

    form_id = form_id
    user_id = verify_token(auth)

    if dbu.check_form_completed(form_id, user_id['user_id']):
        return True
    return False


@app.post("/auth/register")
async def register(user_details: bm.Register):
    user_details = user_details.dict()

    user_id = dbu.register_user(user_details)
    data = {
        'user_id': user_id
    }

    return get_token(data)


@app.post("/auth/login")
async def login(user_details: bm.Login):
    user_details = user_details.dict()

    email = user_details['email']
    passw = user_details['password']

    user_id = dbu.login_user(email, passw)
    data = {'user_id': user_id}
    if user_id:
        return get_token(data)
    return "Unsuccessful login!"


@app.get("/teszt")
async def teszt():
    return "ok"


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def get_token(data: dict):
    # data to be signed using token
    token = create_access_token(data=data)
    return {'token': token}


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return -1
