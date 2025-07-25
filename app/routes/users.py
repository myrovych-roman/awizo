from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User, Role
from app.services.auth import get_password_hash

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/users", response_class=HTMLResponse)
def get_users(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    return templates.TemplateResponse("user_management.html", {"request": request, "users": users})

@router.post("/users/create", response_class=RedirectResponse)
def create_user(db: Session = Depends(get_db), username: str = Form(...), password: str = Form(...), role: str = Form(...), firm_name: str = Form(None), full_name: str = Form(None)):
    hashed_password = get_password_hash(password)
    user = User(username=username, hashed_password=hashed_password, role=role, firm_name=firm_name, full_name=full_name)
    db.add(user)
    db.commit()
    return RedirectResponse(url="/users", status_code=303)

@router.get("/users/{user_id}/delete", response_class=RedirectResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return RedirectResponse(url="/users", status_code=303)
