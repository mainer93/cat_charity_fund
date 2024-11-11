Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:mainer93/cat_charity_fund.git
```

```
cd cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Заполните файл .env:

```
APP_TITLE=Фонд поддержки котиков
APP_DESCRIPTION=Приложение для Благотворительного фонда поддержки котиков
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db
SECRET=SECRET_KEY
FIRST_SUPERUSER_EMAIL=superuser@example.com
FIRST_SUPERUSER_PASSWORD=yourpassword
```

Выполните все неприменённые миграции через команду:

```
alembic upgrade head
```

Запустите проект:

```
uvicorn app.main:app --reload
```