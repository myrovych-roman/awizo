from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.avization import Avization, AvizationStatus, AvizationType
from app.models.user import User
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/avizations/create", response_class=HTMLResponse)
def create_avization_form(request: Request):
    return templates.TemplateResponse("avization_form.html",
                                      {"request": request, "avization_types": [item.value for item in AvizationType]})


@router.post("/avizations/create")
def create_avization(request: Request, db: Session = Depends(get_db), car_number: str = Form(...),
                     driver_name: str = Form(...), firm_name: str = Form(...), avization_type: str = Form(...),
                     comment: str = Form(None)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login")

    avization = Avization(
        car_number=car_number,
        driver_name=driver_name,
        firm_name=firm_name,
        date_time=datetime.now(),
        avization_type=avization_type,
        comment=comment,
        user_id=user_id
    )
    db.add(avization)
    db.commit()
    return RedirectResponse(url="/avizations/search", status_code=303)


@router.get("/avizations/search", response_class=HTMLResponse)
def search_avizations_form(request: Request, db: Session = Depends(get_db)):
    avizations = db.query(Avization).all()
    return templates.TemplateResponse("avization_search.html", {"request": request, "avizations": avizations})


@router.post("/avizations/search", response_class=HTMLResponse)
def search_avizations(request: Request, db: Session = Depends(get_db), search: str = Form(...),
                      search_by: str = Form(...)):
    query = db.query(Avization)
    if search_by == "car_number":
        query = query.filter(Avization.car_number.contains(search))
    elif search_by == "driver_name":
        query = query.filter(Avization.driver_name.contains(search))
    elif search_by == "firm_name":
        query = query.filter(Avization.firm_name.contains(search))
    elif search_by == "user_full_name":
        query = query.join(User).filter(User.full_name.contains(search))

    avizations = query.all()
    return templates.TemplateResponse("avization_search.html", {"request": request, "avizations": avizations})


@router.get("/avizations/{avization_id}/delete")
def delete_avization(request: Request, avization_id: int, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login")

    avization = db.query(Avization).filter(Avization.id == avization_id).first()
    if avization:
        db.delete(avization)
        db.commit()
    return RedirectResponse(url="/avizations/search", status_code=303)


@router.get("/avizations/{avization_id}/edit", response_class=HTMLResponse)
def edit_avization_form(request: Request, avization_id: int, db: Session = Depends(get_db)):
    avization = db.query(Avization).filter(Avization.id == avization_id).first()
    return templates.TemplateResponse("avization_edit.html", {"request": request, "avization": avization,
                                                              "avization_types": [item.value for item in AvizationType],
                                                              "avization_statuses": [item.value for item in
                                                                                     AvizationStatus]})


@router.post("/avizations/{avization_id}/edit")
def edit_avization(request: Request, avization_id: int, db: Session = Depends(get_db), car_number: str = Form(...),
                   driver_name: str = Form(...), firm_name: str = Form(...), avization_type: str = Form(...),
                   status: str = Form(...), comment: str = Form(None)):
    avization = db.query(Avization).filter(Avization.id == avization_id).first()
    if avization:
        avization.car_number = car_number
        avization.driver_name = driver_name
        avization.firm_name = firm_name
        avization.avization_type = avization_type
        avization.status = status
        avization.comment = comment
        db.commit()
    return RedirectResponse(url="/avizations/search", status_code=303)
