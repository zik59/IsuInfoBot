import asyncio
import logging
import sys

from aiohttp import ClientSession
from lxml import html

from isu_info_bot import config
from isu_info_bot.services.students import students_table, create_engine


logging.basicConfig(filename=f"{config.BASE_DIR}/logs/scraper.log",
                    filemode='w',
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))

login_url = "https://isu.smtu.ru/login/"
groups_url = 'https://isu.smtu.ru/students_groups_card_list/'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36\
                (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
}


async def get_hidden_input(session: ClientSession, url: str, **kwargs) -> str:
    async with session.get(url, **kwargs) as response:
        tree = html.fromstring(await response.text())
        hidden_input = tree.xpath("//input[@name='form_num']/@value")
        return hidden_input


async def login(session: ClientSession, url: str, **kwargs) -> None:
    payload = {'form_num': await get_hidden_input(session, url, **kwargs),
               'login': config.LOGIN,
               'password': config.PASSWORD
               }
    response = await session.post(url, data=payload, **kwargs)
    logger.info(f"login {response.status}")


async def get_groups(session: ClientSession, url: str, **kwargs) -> list:
    async with session.get(url, **kwargs) as response:
        tree = html.fromstring(await response.text())
        groups = tree.xpath('//div[@class="panel-body"]//a/text()')
        return groups


async def get_students_from_html(html_tree: str) -> list:
    students = html_tree.xpath('//tr//td[last()]/text()')
    students = _filtered_list(students)
    return sorted(students)


async def get_isu_ids_from_html(html_tree: str) -> list:
    isu_id = html_tree.xpath('//tr/td[2]//text()')
    return isu_id


async def get_image(isu_id: str) -> str:
    return f'/images/isu_person/small/p{isu_id}.jpg'


async def get_group_url(group: str):
    if group.startswith('М'):
        return f'https://isu.smtu.ru/students_groups_card_view/{group[1:]}/'
    return f'https://isu.smtu.ru/students_groups_card_view/{group}/'


async def get_all_info(session: ClientSession, **kwargs):
    groups = await get_groups(session, groups_url, **kwargs)

    for group in groups:
        url = await get_group_url(group)

        tree = await make_html_tree(session, url, headers=headers)

        students = await get_students_from_html(tree)
        isu_ids = await get_isu_ids_from_html(tree)

        for i, student in enumerate(students):
            image = await get_image(isu_ids[i])
            data = [{'isu_id': isu_ids[i],
                     'variant': f'{i+1}',
                     'isu_group': group,
                     'image': image,
                     'name': student}]
            yield data

        await asyncio.sleep(0.1)


async def make_html_tree(session: ClientSession, url: str, **kwargs):
    async with session.get(url, **kwargs) as response:
        logger.info(f"{url} {response.status}")
        tree = html.fromstring(await response.text())
        return tree


async def save_to_db(all_info: list) -> None:
    engine = await create_engine()
    async with engine.begin() as conn:
        async for info in all_info:
            await conn.execute(students_table.insert(), info)


def _filtered_list(students: list) -> None:
    for i in range(len(students)):
        students[i] = ''.join(filter(_filter_name, students[i]))
    return list(filter(None, students))


def _filter_name(elem: str) -> bool:
    if elem == " ":
        return True
    return elem.isalnum()


async def main():
    async with ClientSession() as sess:
        await login(sess, login_url, headers=headers)
        all_info = get_all_info(sess, headers=headers)
        await save_to_db(all_info)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception:
        import traceback

        logger.warning(traceback.format_exc())
