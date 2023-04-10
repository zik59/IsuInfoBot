import asyncio
import os

from aiohttp import ClientSession

from isu_info_bot import config
from isu_info_bot.services.students import students_table, create_engine, select


url_prefix = 'https://isu.smtu.ru'


async def load_images():
    engine = await create_engine()
    async with engine.connect() as conn:
        async with ClientSession() as session:
            images = await conn.execute(select(students_table.c.image))
            for image in images.fetchall():
                url = f"{url_prefix}/{image[0]}"
                response = await session.get(url)
                if response.status == 200:
                    filename = _create_dir(image[0])
                    with open(filename, 'wb') as file:
                        file.write(await response.read())
                else:
                    filename = _create_dir(image[0])
                    os.system(f'cp {config.BASE_DIR}/images/placeholder.jpg {filename}')


def _create_dir(image: str) -> str:
    filename = f'{config.BASE_DIR}/{image}'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    return filename


if __name__ == '__main__':
    asyncio.run(load_images())
