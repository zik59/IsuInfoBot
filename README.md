# IsuInfoBot

## Команды бота:

- `/start` — приветственное сообщение
- `/help` — справка
- `/group` - в какой группе студент
- `/variant` - студенты с таким вариантом

## Запуск

Скопируйте `.env.template` в `.env` и отредактируйте `.env` файл, заполнив в нём все переменные окружения:

```bash
cp isuInfoBot/.env.template isuInfoBot/.env
```
Виртуальное окружение

sudo apt install python3.8-venv
python3 -m venv /venv
source /venv/bin/activate

Установка зависимостей и запуск бота:

```bash
pip install -r /path/to/requirments.txt
python3 -m isu_info_bot
```

Перед запуском нужно пропарсить сайт и записать данные в бд с помощью:

```bash
python3 isu_info_bot/isu_parser/scraper.py
python3 isu_info_bot/csv_to_db.py
```

## Ideas
- Сделать очевидный для пользователя прием параметров (возможно с помощью кнопок)
- Состояния при навигации
- редис и кэширование
- ввод имени с ошибками(левенштайн, триангуляция)
