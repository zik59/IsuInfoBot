import sqlite3
from typing import Optional

from isu_info_bot import config


database = config.SQLITE_DB_FILE


def get_group_by_name(name: str) -> set:
    conn = _create_connection(database)
    with conn:
        curs = conn.cursor()
        curs.execute("SELECT isu_group, full_name FROM students")

        groups = set()

        for row in curs.fetchall():
            if name in row[1]:
                groups.add(row[0])
        return sorted(list(groups))


def get_students_by_variant(variant: int, faculty=None, course=None) -> dict:
    conn = _create_connection(database)
    with conn:
        curs = conn.cursor()
        curs.execute("SELECT order_in_isu_list, isu_group, full_name FROM students")

        people = {}
        for row in curs.fetchall():
            if row[0] == variant:
                if people.get(row[1]) is None:
                    people[row[1]] = []
                people[row[1]].append(row[2])
        return people


def _create_connection(db_file: str) -> sqlite3.Connection:
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception:
        raise

    return conn