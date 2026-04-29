# Minimal Flask Blog

Простой блог-движок без CMS:

- публичная витрина с постами;
- админка с логином/паролем;
- создание, редактирование и удаление постов;
- базовые настройки сайта;
- локально `SQLite`, в проде можно переключиться на `MySQL` через `DATABASE_URL`.

## Запуск локально

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

Приложение поднимется на `http://127.0.0.1:5000`.

Админка: `http://127.0.0.1:5000/admin`

Логин по умолчанию:

- `admin`
- `admin`

Лучше сразу переопределить переменные окружения:

```bash
export SECRET_KEY="change-me"
export ADMIN_USERNAME="editor"
export ADMIN_PASSWORD="strong-password"
```

## Переход на MySQL в проде

Достаточно задать `DATABASE_URL`, например:

```bash
export DATABASE_URL="mysql+pymysql://user:password@host:3306/blog_db"
```

Для MySQL понадобится добавить драйвер, например:

```bash
pip install pymysql
```
