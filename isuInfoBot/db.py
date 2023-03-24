import sqlite3
import csv

import config


conn = sqlite3.connect(config.SQLITE_DB_FILE)
cursor = conn.cursor()

cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS students (
    order_in_isu_list INT,
    isu_group INT,
    full_name TEXT
    )
    '''
    )
# truncation - удаляем данные из таблицы, не удаляю саму таблицу
cursor.execute("DELETE FROM students")

conn.commit()

file_name = 'isuInfo/students.csv'

with open(file_name, 'r', encoding='utf-8', newline='') as csv_file:
    data_reader = csv.reader(csv_file, delimiter=" ", quotechar='|')

    for row in data_reader:
        cursor.execute(
            "INSERT INTO students VALUES(?,?,?)", row
        )

conn.commit()
conn.close()
