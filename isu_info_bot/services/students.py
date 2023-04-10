import re
import sqlite3
from typing import Optional

import sqlalchemy as db
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine

from isu_info_bot import config


database = config.SQLITE_DB_FILE
meta = db.MetaData()
students_table = db.Table('students', meta,
                          db.Column("isu_id", db.Text(), primary_key=True),
                          db.Column("variant", db.String(2)),
                          db.Column("isu_group", db.String(10)),
                          db.Column("image", db.Text()),
                          db.Column("name", db.String(70))
                          )


async def create_engine() -> db.Engine:
    return create_async_engine(
        "postgresql+asyncpg://postgres:postgres@localhost/postgres",
        echo=True,
    )


def get_group_by_name(student_name: str) -> dict:
    conn = _create_connection(database)
    with conn:
        curs = conn.cursor()
        curs.execute("SELECT isu_group, name FROM students")

        groups = {}

        for isu_group, name in curs.fetchall():
            if student_name.lower() in name.lower():
                groups[isu_group] = name

        return _paginate_dict(groups)


def get_students_by_variant(variant: str, faculty: Optional[str] = None, course: Optional[str] = None) -> dict:
    conn = _create_connection(database)
    with conn:
        curs = conn.cursor()
        curs.execute("SELECT variant, isu_group, name FROM students")

        pattern = 'М?{faculty}{course}[0-9]{{2}}$'.format(faculty=faculty or '\d', course=course or '\d')
        students = {}

        for var, isu_group, name in curs.fetchall():
            if var == variant and re.fullmatch(pattern, isu_group):
                students[isu_group] = name

        return _paginate_dict(students)


def _paginate_dict(dictionary: dict) -> dict:
    pages = {}
    i = 1
    for item in dictionary.items():
        if not pages.get(i):
            pages[i] = {}
        pages[i].update({item[0]: item[1]})
        if len(pages[i]) == config.PAGE_SIZE:
            i += 1
    return pages


def _create_connection(db_file: str) -> sqlite3.Connection:
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception:
        raise

    return conn
