from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter()


@router.post("/logout")
def logout(request: Request, csrf_token: str = Form(...)):

    if csrf_token != request.session.get("csrf_token"):
        return HTMLResponse(content="Invalid CSRF Token", status_code=403)

    request.session.clear()

    return RedirectResponse(url="/login/", status_code=303)
