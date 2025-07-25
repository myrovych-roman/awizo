from fastapi import FastAPI
from app.routes import auth, avization, users, settings
from starlette.middleware.sessions import SessionMiddleware
from app.config import SECRET_KEY

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

app.include_router(auth.router)
app.include_router(avization.router)
app.include_router(users.router)
app.include_router(settings.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Avization Control System"}
