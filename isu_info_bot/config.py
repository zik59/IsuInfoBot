import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
LOGIN = os.getenv("LOGIN", "")
PASSWORD = os.getenv("PASSWORD", "")

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"

PAGE_SIZE = 10

GROUP_CALLBACK_PATTERN = "group_"
STUDENT_CALLBACK_PATTERN = "student_"
VARIANT_CALLBACK_PATTERN = "variant_"
