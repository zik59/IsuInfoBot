import sqlite3
import csv

import config


file_name = str(config.BASE_DIR) + '/students.csv'


def create_connection(db_file: str) -> sqlite3.Connection:
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception:
        raise

    return conn


def create_table(cursor: sqlite3.Cursor) -> None:
    cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS students (
    variant VARCHAR(2),
    isu_group VARCHAR(10),
    name VARCHAR(70)
    )
    '''
    )


def truncate(cursor: sqlite3.Cursor) -> None:
    """truncation - удаляем данные из таблицы, не удаляю саму таблицу"""
    cursor.execute("DELETE FROM students")


def insert_into_table(cursor: sqlite3.Cursor) -> None:
    with open(file_name, 'r', encoding='utf-8', newline='') as csv_file:
        data_reader = csv.reader(csv_file, delimiter=" ", quotechar='|')

        for row in data_reader:
            cursor.execute(
                "INSERT INTO students VALUES(?,?,?)", row
            )
 

def main():
    with create_connection(config.SQLITE_DB_FILE) as conn:
        cursor = conn.cursor()
        create_table(cursor)
        truncate(cursor)
        conn.commit()
        insert_into_table(cursor)
        conn.commit()


if __name__ == "__main__":
    main()
