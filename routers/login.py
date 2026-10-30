from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from database import SessionLocal
from models import User
from auth import verify_password

import secrets

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/login/", response_class=HTMLResponse)
def login_page(request: Request):

    return templates.TemplateResponse(request=request, name="login.html", context={})


@router.post("/submit/")
def login_submit(request: Request, email: str = Form(...), password: str = Form(...)):

    db = SessionLocal()

    user = db.query(User).filter(User.email == email).first()

    db.close()

    if not user:
        return RedirectResponse(url="/login/", status_code=303)

    if not verify_password(password, user.password):
        return RedirectResponse(url="/login/", status_code=303)

    request.session["user"] = user.email
    request.session["role"] = user.role

    request.session["csrf_token"] = secrets.token_hex(16)

    return RedirectResponse(url="/welcome", status_code=303)
