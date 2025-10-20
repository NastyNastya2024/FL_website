from pathlib import Path
from typing import Optional
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, constr
from .storage import init_storage, save_submission


DATA_DIR = Path(__file__).resolve().parent / "data"
DB_PATH = DATA_DIR / "forms.db"


class ContactForm(BaseModel):
    email: EmailStr
    phone: constr(strip_whitespace=True, min_length=5, max_length=50)
    subject: constr(strip_whitespace=True, min_length=1, max_length=200)
    message: constr(strip_whitespace=True, min_length=1, max_length=1000)
    privacy_consent: bool
    marketing_consent: Optional[bool] = False
    form_version: Optional[str] = "v1.0"


app = FastAPI(title="Forms API", version="1.0.0")

# CORS: adjust origins if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"]
)


@app.on_event("startup")
def on_startup() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    init_storage(DB_PATH)


@app.post("/api/forms/contact")
async def submit_contact(form: ContactForm, request: Request):
    client_ip = request.client.host if request.client else ""
    user_agent = request.headers.get("user-agent", "")

    try:
        save_submission(
            db_path=DB_PATH,
            ip=client_ip,
            user_agent=user_agent,
            form_version=form.form_version or "v1.0",
            email=str(form.email),
            phone=form.phone,
            subject=form.subject,
            message=form.message,
            privacy_consent=bool(form.privacy_consent),
            marketing_consent=bool(form.marketing_consent or False),
        )
    except Exception as exc:  # pragma: no cover
        raise HTTPException(status_code=500, detail="Storage error") from exc

    return {"status": "ok"}


