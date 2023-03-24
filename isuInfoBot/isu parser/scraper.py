import csv
import os
import time
import logging

import requests
from dotenv import load_dotenv
from lxml import html


load_dotenv()

logging.basicConfig(filename="scraper.log", filemode='w', level=logging.INFO)
logger = logging.getLogger(__name__)


login_url = "https://isu.smtu.ru/login/"

# Запросик на страничку с логином
session_requests = requests.session()
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Referer': login_url
}
result = session_requests.get(login_url, headers=headers)

# Нужно пропарсить страницу и захвататить невидимую форму
tree = html.fromstring(result.text)
hidden_input = tree.xpath("//input[@name='form_num']/@value")

# Авторизуемся очередным запросом
payload = {
    'form_num': hidden_input,
    'login': os.getenv("LOGIN", ""),
    'password': os.getenv("PASSWORD", "")
}

result = session_requests.post(login_url, data=payload, headers=headers)

# Делаем запрос для списка групп
groups_url = 'https://isu.smtu.ru/students_groups_card_list/'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}

result = session_requests.get(groups_url, headers=headers)

# Парсим номера групп
all_groups = []
htmlElem = html.document_fromstring(result.content)
groups = htmlElem.find_class("gr")
for group in groups:
    all_groups.extend(group.xpath('//a[@class="toggle-vis btn btn-default black"]/text()'))

#print(sorted(list(set(all_groups)))) #489 групп(много запросов)


def filter_name(elem):
            if elem == " ":
                return True
            return elem.isalnum()

# По каждому номеру отправляем запросик 
file_name = 'isuInfo/students.csv'
with open(file_name, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_ALL)

    all_groups = sorted(list(set(all_groups)))
    for group in all_groups:
        url = f'https://isu.smtu.ru/students_groups_card_view/{group}/'
        response = session_requests.get(url, headers=headers)
        htmlElem = html.document_fromstring(response.content)
        logger.info([group, response.status_code])

        studentsX = htmlElem.find_class("gradeX")
        studentsA = htmlElem.find_class("gradeA")

        all_students = []

        for X in studentsX:
            all_students.extend(X.xpath('//tr[@class="gradeX"]//td[last()]/text()'))
                
        for A in studentsA:
            all_students.extend(A.xpath('//tr[@class="gradeA"]//td[last()]/text()'))

        all_students = sorted(list(set(all_students)))
        num_of_empty_strings = 0
        for i in range(len(all_students)):
            all_students[i] = ''.join(filter(filter_name, all_students[i]))
            if not all_students[i]:
                num_of_empty_strings += 1
                continue
            writer.writerow([i+1-num_of_empty_strings, group, all_students[i]])
        time.sleep(3) # Чтобы случайно не заддосить
