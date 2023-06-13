# Лекция 2

## Инструкция создания нового модуля

### 1. Определитесь с названием модуля. Для примера возьмум `posts`

### 2. Создаем папку `./app/posts`

### 3. Создадим каркас модуля

- Файл `./app/posts/__init__.py`;
- Файл `./app/posts/service.py`;
- Папка `./app/posts/router/`;
- Файл `./app/posts/router/__init__.py`;

Должна быть следующая структура проекта:

```
.
└── app
    ├── auth
    │   └── ...
    └── posts
        ├── __init__.py
        ├── service.py
        └── router
            └── __init__.py

```

## 4. Заполним service.py

Файл `service.py` содержит класс `Service` который содержит все зависимости модуля (репозиторий, внешние сервисы).

Пока что у нас нет зависимостей, поэтому он пустой.

```py
from app.config import database


class Service:
    def __init__(self):
        pass


def get_service():
    svc = Service()
    return svc
```

## 5. Заполним router.py

Данный код определяет под-модуль для API и импортирует все файлы в текущей директории начинающиеся с `router_`.

Это понадобится чтобы в дальнейшем создавать новые роутеры `router_create_post.py`, `router_get_posts.py` и т.д.

```py
from fastapi import APIRouter

from app.utils import import_routers

router = APIRouter()
import_routers(__name__)
```
