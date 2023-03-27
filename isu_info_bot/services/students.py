import re
import sqlite3
from typing import Optional

from isu_info_bot import config


database = config.SQLITE_DB_FILE


def get_group_by_name(student_name: str) -> list:
    conn = _create_connection(database)
    with conn:
        curs = conn.cursor()
        curs.execute("SELECT isu_group, name FROM students")

        groups = {}

        for isu_group, name in curs.fetchall():
            if student_name in name:
                groups[isu_group] = name
        pages = _paginate_dict(groups)
        return pages


def get_students_by_variant(variant: str, faculty: Optional[str]=None, course: Optional[str]=None) -> dict:
    conn = _create_connection(database)
    with conn:
        curs = conn.cursor()
        curs.execute("SELECT variant, isu_group, name FROM students")
        
        students = {}
        pattern = 'М?{faculty}{course}[0-9]{{2}}$'.format(faculty=faculty or '\d', course=course or '\d')
        for var, isu_group, name in curs.fetchall():
            if var == variant and re.fullmatch(pattern, isu_group):
                    students[isu_group] = name
        pages = _paginate_dict(students)
        return pages


def _paginate_dict(dict_name: dict) -> dict:
    pages = {}
    i = 1
    for item in dict_name.items():
        if not pages.get(i):
            pages[i] = {}
        pages[i].update({item[0]:item[1]})
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
