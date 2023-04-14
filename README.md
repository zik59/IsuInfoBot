# IsuInfoBot

## Команды бота:

- `/start` - приветственное сообщение
- `/help` - справка
- `/group` - список группы
- `/student` - поиск студентов по имени
- `/variant` - поиск студентов по варианту
- `/cancel` - отмена текущего действия

## Запуск

Скопируйте `.env.template` в `.env` и отредактируйте `.env` файл, заполнив в нём все переменные окружения:

```bash
cp isuInfoBot/.env.template isuInfoBot/.env
```
Виртуальное окружение:

```bash
sudo apt install python3.8-venv
python3 -m venv /venv
source /venv/bin/activate
```

Установка зависимостей и сборка:

```bash
pip install -r /path/to/requirments.txt
docker-compose up
```

Перед запуском нужно пропарсить сайт, записать данные в бд, а также загрузить картинки:

```bash
python3 isu_info_bot/isu_parser/scraper.py
python3 isu_info_bot/isu_parser/load_images.py
```

Запуск бота:

```bash
python3 -m isu_info_bot
```