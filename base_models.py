from pydantic import BaseModel


class Login(BaseModel):
    email: str
    password: str


class Register(BaseModel):
    name: str
    email: str
    password: str


class Submission(BaseModel):
    form_id: str
    options: list


class FormCreation(BaseModel):
    name: str
    desc: str
    options: list
    active: bool
