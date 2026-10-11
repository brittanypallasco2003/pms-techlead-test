import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(
    dotenv_path=Path(__file__).resolve().parent.parent / ".env",
    override=False,
    encoding="utf-8-sig",
)

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017").strip()
DATABASE = os.getenv("DATABASE", "ada_exam").strip()
REPORT_TOKEN = os.getenv("REPORT_TOKEN", "demo-only-not-a-real-secret").strip()

_allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:4200")
ALLOWED_ORIGINS = [
    origin.strip()
    for origin in _allowed_origins.split(",")
    if origin.strip()
]
