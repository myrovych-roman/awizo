from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/settings", response_class=HTMLResponse)
def get_settings(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request})
