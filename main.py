from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from database import Base, engine
from exception_handlers import custom_http_exception_handler

from routers.register import router as register_router
from routers.login import router as login_router
from routers.welcome import router as welcome_router
from routers.logout import router as logout_router

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="my-secret-key")

app.add_exception_handler(StarletteHTTPException, custom_http_exception_handler)

Base.metadata.create_all(bind=engine)

app.include_router(register_router)
app.include_router(login_router)
app.include_router(welcome_router)
app.include_router(logout_router)
