from fastapi import FastAPI, Body

app = FastAPI()

forms = {
    "form1": {
        "title": "Sample Form",
        "desc": "This is a sample form.",
        "options": ["Option 1", "Option 2", "Option 3"]
    }
}


@app.get("/get_form_data")
async def get_form_data(auth: str, form_id: str):
    if auth != "token":
        return {"error": "Unauthorized access"}
    return forms[form_id]


created_forms = {}


@app.post("/create_form")
async def create_form(auth: str, form_data: dict = Body(...)):
    if auth != "token":
        return {"error": "Unauthorized access"}
    required_fields = ["title", "desc", "opt"]
    for field in required_fields:
        if field not in form_data:
            return {"error": f"Missing required field: {field}"}

    form_id = len(created_forms) + 1
    created_forms[form_id] = form_data

    return {"form_id": form_id}


form_submissions = {
    "form1": [
        {"name": "pizza", "value": 1},
        {"name": "hamburger", "value": 0},
        {"name": "chocolate", "value": 0}
    ],
    "form2": [
        {"name": "pizza", "value": 0},
        {"name": "hamburger", "value": 1},
        {"name": "chocolate", "value": 0}
    ]
}


@app.get("/get_form_submission")
async def get_form_submission(auth: str, form_id: str):
    if auth != "token":
        return {"error": "Unauthorized access"}

    if form_id not in form_submissions:
        return {"error": "Form not found"}

    return form_submissions[form_id]


users_db = {}


@app.post("/register")
async def register(user_details: dict):
    if "name" not in user_details:
        return {"error": "Name is required"}
    elif "email" not in user_details:
        return {"error": "E-mail is required"}
    elif "phone" not in user_details:
        return {"error": "Phone is required"}
    elif "pass" not in user_details:
        return {"error": "Password is required"}
    elif "role" not in user_details:
        return {"error": "Role is required"}

    token = generate_token(user_details["email"])

    users_db[user_details["email"]] = user_details

    return {"token": token}


def generate_token(email):
    return email + "_token"


users_db1 = {
    "emejl": {"pass": "example_password"}
}


@app.post("/login")
async def login(user_details: dict):
    if "email" not in user_details:
        return {"error": "E-mail is required"}
    elif "pass" not in user_details:
        return {"error": "Password is required"}

    email = user_details["email"]
    passw = user_details["pass"]

    if email in users_db1 and users_db1[email]["pass"] == passw:
        token = generate_token(email)
        return {"token": token}
    else:
        return {"error": "Invalid email or password!"}


@app.get("/teszt")
async def teszt():
    return "ok"
