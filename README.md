# Forms backend (FastAPI + SQLite)

## Run locally

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

API: POST /api/forms/contact

Payload (JSON):
- email, phone, subject, message, privacy_consent, marketing_consent (optional), form_version (optional)

DB file: backend/data/forms.db

## Deploy
- Run behind reverse proxy (nginx) at /api/
- Ensure backend/data writable
- Configure CORS to your domain

