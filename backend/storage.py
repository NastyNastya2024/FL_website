from pathlib import Path
import sqlite3


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS submissions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  ip TEXT,
  user_agent TEXT,
  form_version TEXT,
  email TEXT,
  phone TEXT,
  subject TEXT,
  message TEXT,
  privacy_consent INTEGER NOT NULL,
  marketing_consent INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_submissions_created_at ON submissions(created_at);
"""


def init_storage(db_path: Path) -> None:
    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(SCHEMA_SQL)
        conn.commit()
    finally:
        conn.close()


def save_submission(
    db_path: Path,
    ip: str,
    user_agent: str,
    form_version: str,
    email: str,
    phone: str,
    subject: str,
    message: str,
    privacy_consent: bool,
    marketing_consent: bool,
) -> None:
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            """
            INSERT INTO submissions (
              ip, user_agent, form_version, email, phone, subject, message,
              privacy_consent, marketing_consent
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                ip,
                user_agent,
                form_version,
                email,
                phone,
                subject,
                message,
                1 if privacy_consent else 0,
                1 if marketing_consent else 0,
            ),
        )
        conn.commit()
    finally:
        conn.close()


