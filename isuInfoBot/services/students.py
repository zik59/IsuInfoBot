import sqlite3


database = "isuInfo/db.sqlite3"

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)

    return conn


def get_group_by_name(name: str):
    conn = create_connection(database)
    with conn:
        curs = conn.cursor()
        curs.execute("SELECT isu_group, full_name FROM students")

        groups = []

        for row in curs.fetchall():
            if name in row[1]:
                groups.append(row[0])
        return groups


def get_students_by_variant(variant: int):
    conn = create_connection(database)
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
