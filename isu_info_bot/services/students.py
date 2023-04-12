import re
from typing import Optional

import sqlalchemy as db
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine

from isu_info_bot import config


meta = db.MetaData()
students_table = db.Table('students', meta,
                          db.Column("isu_id", db.Text()),
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


async def get_students_by_group(group: str) -> dict:
    engine = await create_engine()
    async with engine.connect() as conn:
        query = await conn.execute(select(students_table.c.variant,
                                          students_table.c.name,
                                          students_table.c.image).where(students_table.c.isu_group == group))
        students = {}

        for variant, name, image in query.fetchall():
            students[variant] = name, image

    return _paginate_dict(students)


async def get_students_by_name(student_name: str) -> dict:
    engine = await create_engine()
    async with engine.connect() as conn:
        query = await conn.execute(select(students_table.c.isu_group,
                                          students_table.c.name,
                                          students_table.c.image))
        students = {}

        for isu_group, name, image in query.fetchall():
            if student_name.lower() in name.lower():
                students[isu_group] = name, image

        return _paginate_dict(students)


async def get_students_by_variant(variant: str, faculty: Optional[str] = None, course: Optional[str] = None) -> dict:
    engine = await create_engine()
    async with engine.connect() as conn:
        query = await conn.execute(select(students_table.c.isu_group,
                                          students_table.c.name,
                                          students_table.c.image).where(students_table.c.variant == variant))
        pattern = 'М?{faculty}{course}[0-9]{{2}}$'.format(faculty=faculty or '\d', course=course or '\d')

        students = {}
        for isu_group, name, image in query.fetchall():
            students[isu_group] = name, image

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
