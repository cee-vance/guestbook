from fastapi import FastAPI, Request, Depends, Form, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import engine, SessionLocal  # Absolute import
from app import models  # Absolute import

from pathlib import Path
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Automatically create database tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cloud Guestbook")



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_home(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"request": request}
    )


@app.post("/sign")
def sign_guestbook(name: str = Form(...), db: Session = Depends(get_db)):
    entry = models.GuestbookEntry(name=name)
    db.add(entry)
    db.commit()
    return RedirectResponse(url="/list", status_code=303)


@app.get("/list", response_class=HTMLResponse)
def list_entries(
        request: Request,
        limit: int = Query(5, ge=1, le=50),
        offset: int = Query(0, ge=0),
        db: Session = Depends(get_db)
):
    entries = db.query(models.GuestbookEntry).order_by(models.GuestbookEntry.timestamp.desc()).offset(offset).limit(
        limit).all()
    total_entries = db.query(models.GuestbookEntry).count()

    return templates.TemplateResponse(
        "list.html",
        {
            "request": request,
            "entries": entries,
            "limit": limit,
            "offset": offset,
            "total_entries": total_entries
        }
    )


@app.get(path="/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}, 500
