from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/welcome", response_class=HTMLResponse)
def welcome(request: Request):

    user = request.session.get("user")

    if not user:
        return RedirectResponse(url="/login/", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="welcome.html",
        context={"username": user, "csrf_token": request.session.get("csrf_token")},
    )
