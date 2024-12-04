# FastAPI Currency Converter

## Описание

Это проект представляет мини версию delivery club
В проекте реализовал паттерн UnitOfWork и Repository
UOW взял ради сохранения AСID. Т.к. в проекте есть платежные операции
Для поиска дучше использовать elasticsearch с fuzzy поиском
Сделана регистрация и авторизация по bearer токену
Проект получился объемным как для тестового задания
Но все это сделано чтобы была возможность внедрять и расширять проект без каких либо проблем ;)

На весь проект у меня ушло около 5 часов. С документацией, тестами и перерывами

Проект покрыт тестами, но не полностью
Тесты в докере не раюотают. Там их нужно отдельно настраивать.
Для запуска тестов удалить Dockerfile

```bash
docker compose up
```

```bash
poetry install
```

```bash
poetry shell
```

После чего из корневой папки

```bash
fastapi dev app/main.py
```

И после

```bash
pytest
```

- **FastAPI**: для создания веб-приложения.
- **SQLalchemy**: ORM для работы с базой (ORM версия, не CORE) .
- **Alembic**: миграции sql .
- **Pydantic Settings**: для управления настройками.
- **Uvicorn**: как ASGI сервер.
- **HTTPX**: для выполнения HTTP-запросов.
- **Pytest**: среда выполнения тестов.
- **Docker**: виртуализация.

Проект завернут в Docker контейнер для удобства.

## Установка и запуск

### Клонирование репозитория

```bash
git https://github.com/krasniy-1889/social_systems_delivery.git
cd social_systems_delivery
```

### Запуск контейнера

```bash
docker build -t social_systems_delivery .
docker run --name social_systems_delivery -p 8000:8000 social_systems_delivery
```

### Открыть ссылку

`http://0.0.0.0:8000/docs`
