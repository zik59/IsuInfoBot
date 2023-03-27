import csv
import time
import logging

import requests
from requests import Session
from lxml import html

from isu_info_bot import config


logging.basicConfig(filename="scraper.log", filemode='w',
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

csv_file_name = f'{config.BASE_DIR}/students.csv'

login_url = "https://isu.smtu.ru/login/"
groups_url = 'https://isu.smtu.ru/students_groups_card_list/'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}


def start_session() -> Session:
    return requests.session()


def get_hidden_input(session: Session, url: str, headers: dict) -> str:
    tree = make_tree(session, url, headers)
    hidden_input = tree.xpath("//input[@name='form_num']/@value")
    return hidden_input


def login(session: Session, url: str, headers: dict) -> None:
    payload = {
    'form_num': get_hidden_input(session, url, headers),
    'login': config.LOGIN,
    'password': config.PASSWORD
    }
    session.post(url, data=payload, headers=headers)


def get_list_of_groups(session: Session, url: str, headers: dict) -> list:
    tree = make_tree(session, url, headers)
    all_groups = tree.xpath('//a[@class="toggle-vis btn btn-default black"]/text()')
    return all_groups


def get_list_of_students_in_group(session: Session, url: str, headers:dict) -> list:
    tree = make_tree(session, url, headers)
    students_in_group = tree.xpath('//tr[@class="gradeX"]//td[last()]/text()')
    students_in_group.extend(tree.xpath('//tr[@class="gradeA"]//td[last()]/text()'))
    filter_list(students_in_group)
    return sorted(students_in_group)


def get_all_students(session: Session, headers:dict, all_groups: list) -> dict:
    all_students = {}

    for group in all_groups:
        if group.startswith('М'):
            url = f'https://isu.smtu.ru/students_groups_card_view/{group[1:]}/'
        else:
            url = f'https://isu.smtu.ru/students_groups_card_view/{group}/'

        students_in_group = get_list_of_students_in_group(session, url, headers)
        all_students[group] = students_in_group
        time.sleep(1)

    return all_students


def make_tree(session: Session, url: str, headers: dict):
    response = session.get(url, headers=headers)
    tree = html.fromstring(response.text)
    return tree


def filter_list(students_in_group: list) -> None:
    for i in range(len(students_in_group)):
        students_in_group[i] = ''.join(filter(filter_name, students_in_group[i]))
    students_in_group = list(filter(None, students_in_group))


def filter_name(elem: str) -> bool:
    if elem == " ":
        return True
    return elem.isalnum()


def write_to_csv(file_name: str, all_students: dict) -> None:
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_ALL)
        for group, students in all_students.items():
            for i in range(len(students)):
                writer.writerow([i+1,group,students[i]])


def main():
    sess = start_session()
    login(sess, login_url, headers)
    all_groups = get_list_of_groups(sess, groups_url, headers)
    all_students = get_all_students(sess, headers, all_groups)
    write_to_csv(csv_file_name, all_students)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        import traceback

        logger.warning(traceback.format_exc())
