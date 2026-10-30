from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr

from database import SessionLocal
from models import User
from auth import hash_password

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
def registration_page(request: Request):

    return templates.TemplateResponse(
        request=request, name="registration.html", context={}
    )


@router.post("/register_user")
def register_user(
    name: str = Form(...), email: EmailStr = Form(...), password: str = Form(...)
):

    db = SessionLocal()

    existing_user = db.query(User).filter(User.email == str(email)).first()

    if existing_user:
        db.close()

        return HTMLResponse(
            content="""
            <h2>Email already registered</h2>
            <a href="/login/">Go to Login Page</a>
            """,
            status_code=400,
        )

    new_user = User(name=name, email=str(email), password=hash_password(password))

    db.add(new_user)
    db.commit()
    db.close()

    return RedirectResponse(url="/login/", status_code=303)
