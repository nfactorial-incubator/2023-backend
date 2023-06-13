# Лекция 2

## Инструкция создания нового модуля

### 1. Определитесь с названием модуля. Для примера возьмем `posts`

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

## 6. Создадим первый роут

Роут создадим в `./app/posts/router/router_change_post.py`.

Определяем что роут доступен через метод `PATCH`.

Даем название ф-ции. Название должно кратко описывать что делает функция, допустим `change_post`.

```py
from . import router

@router.patch("/")
def change_post():
    return {"message": "nFactorial School"}
```

## 7. Добавим ожидаемый результат

Чтобы в swagger показывать какой будет ожидаемый ответ, мы должны определить модель ответа.

Создаем класс `ChangePostResponse` с ожидаемыми полями, в нашем случае `message`.

Обратите внимание что название ф-ции `change_post`, а название класса `ChangePostResponse`. Вы должны в дальнейшем придерживаться такого же принципа. Если название ф-ции было бы `create_first_post`, то название класса `CreateFirstPostResponse`.

```py
from app.utils import AppModel

from . import router

class ChangePostResponse(AppModel):
    message: str


@router.patch("/", response_model=ChangePostResponse)
def change_post():
    return {"message": "nFactorial School"}
```

## 8. Подключим наш роутер в API.

Чтобы наш модуль был доступен в API нужно подключить наш новый роутер в главный API объект.

В файле `./app/main.py` сначала импортируем наш роутер, важно чтобы импорты были находились вместе.

```py
# ...

from app.auth.router import router as auth_router
from app.posts.router import router as posts_router # <- наш новый модуль posts

# ...
```

Далее, в конце файла импортируем наш модуль под определенным путем, например под `/posts`.

```py
# ...

app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(posts_router, prefix="/posts", tags=["Posts"]) # <- подключаем модуль posts

# ...
```

Теперь, если запустите API, то наш модуль будет доступен.

## 7. Добавим структуру тела запроса

Чтобы в swagger показывать какое тело запроса роут ожидает, мы должны определить структуру тела.

Создаем класс `ChangePostRequest` с ожидаемыми полями, к примеру мы хотим принимать:
```
{
    "city": "Almaty",
    "message": "Hello"
}
```

Тогда модель класса должна быть следующей:

```py
class ChangePostRequest(AppModel):
    city: str
    message: str
```


Подключим нашу структуру запроса к роуту:

```py
from app.utils import AppModel

from . import router


class ChangePostRequest(AppModel):
    city: str
    message: str


class ChangePostResponse(AppModel):
    message: str


@router.patch("/", response_model=ChangePostResponse)
def change_post(req: ChangePostRequest):
    return {"message": "nFactorial School"}
```

Теперь в swagger будет показывать структуру запроса и структуру ответа.
