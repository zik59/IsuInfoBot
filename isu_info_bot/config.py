import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
LOGIN = os.getenv("LOGIN", "")
PASSWORD = os.getenv("PASSWORD", "")

BASE_DIR = Path(__file__).resolve().parent
SQLITE_DB_FILE = BASE_DIR / "db.sqlite3"
TEMPLATES_DIR = BASE_DIR / "templates"

PAGE_SIZE = 10

VARIANT_CALLBACK_PATTERN = "variant_"
GROUP_CALLBACK_PATTERN = "group_"
