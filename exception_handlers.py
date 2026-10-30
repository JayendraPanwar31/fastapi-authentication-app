from fastapi import Request
from fastapi.responses import HTMLResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse(
            request=request, name="404.html", context={}, status_code=404
        )

    return HTMLResponse(content=str(exc.detail), status_code=exc.status_code)
