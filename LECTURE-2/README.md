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

### 4. Заполним service.py

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

### 5. Заполним router.py

Данный код определяет под-модуль для API и импортирует все файлы в текущей директории начинающиеся с `router_`.

Это понадобится чтобы в дальнейшем создавать новые роутеры `router_create_post.py`, `router_get_posts.py` и т.д.

```py
from fastapi import APIRouter

from app.utils import import_routers

router = APIRouter()
import_routers(__name__)
```

### 6. Создадим первый роут

Роут создадим в `./app/posts/router/router_create_post.py`.

Определяем что роут доступен через метод `POST`.

Даем название ф-ции. Название должно кратко описывать что делает функция, допустим `create_post`.

```py
from . import router

@router.post("/")
def create_post():
    return {"message": "nFactorial School"}
```

### 7. Добавим ожидаемый результат

Чтобы в swagger показывать какой будет ожидаемый ответ, мы должны определить модель ответа.

Создаем класс `CreatePostResponse` с ожидаемыми полями, в нашем случае `message`.

Обратите внимание что название ф-ции `create_post`, а название класса `CreatePostResponse`. Вы должны в дальнейшем придерживаться такого же принципа. Если название ф-ции было бы `create_first_post`, то название класса `CreateFirstPostResponse`.

```py
from app.utils import AppModel

from . import router

class CreatePostResponse(AppModel):
    message: str


@router.post("/", response_model=CreatePostResponse)
def create_post():
    return {"message": "nFactorial School"}
```

### 8. Подключим наш роутер в API.

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

### 9. Добавим структуру тела запроса

Чтобы в swagger показывать какое тело запроса роут ожидает, мы должны определить структуру тела.

Создаем класс `CreatePostRequest` с ожидаемыми полями, к примеру мы хотим принимать:

```
{
    "city": "Almaty",
    "message": "Hello"
}
```

Тогда модель класса должна быть следующей:

```py
class CreatePostRequest(AppModel):
    city: str
    message: str
```

Подключим нашу структуру запроса к роуту:

```py
from app.utils import AppModel

from . import router


class CreatePostRequest(AppModel):
    city: str
    message: str


class CreatePostResponse(AppModel):
    message: str


@router.post("/", response_model=CreatePostResponse)
def create_post(req: CreatePostRequest):
    return {"message": "nFactorial School"}
```

Теперь в swagger будет показывать структуру запроса и структуру ответа.

## Как закрыть роут за авторизацией?

Чтобы роут был доступен только авторизованным пользователям нужно добавить `JWTData` в аргументы роута.

1. Для этого импортируем `Depends`, `JWTData` и `parse_jwt_user_data`.

```py
from fastapi import Depends

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
```

2. Добавляем `JWTData` в аргументы роута:

```py
# ...
def create_post(req: CreatePostRequest, jwt_data: JWTData = Depends(parse_jwt_user_data)):
# ...
```

Но чтобы все не было на одной длинной линии, можно переписать таким образом:

```py
# ...
def create_post(
    req: CreatePostRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
):
# ...
```

Все теперь роут доступен только авторизованным пользователям.

Внутри роута доступна переменная `jwt_data`, в которой хранится id пользователя.

```py
user_id = jwt_data.user_id
```

## Подключение базы данных к модулю

Для того чтобы была возможность работать с базой данных, понадобится сделать две вещи:

1. Создать репозиторий
2. Добавить репозиторий в сервис модуля

> 💡 Репозиторий - это класс для работы с базой данных, методы репозитория будем вызывать внутри роутов

> 💡 Сервис модуля хранит все завимости текущего модуля. На данном этапе мы знакомы только с одной зависимостью - с базой данных.
> Сервис доступен внутри роутов.

### 1. Создаем папку repository `./app/posts/repository`

### 2. Внутри папки создаем два файла

- `__init__.py` - оставляем пустым
- `repository.py`

### 3. Создаем класс репозитория

Мы создаем репозиторий, который взаимодействует с данным `posts`, поэтому назовем наш класс `PostRepository`.

```py
from bson.objectid import ObjectId
from pymongo.database import Database


class PostRepository:
    def __init__(self, database: Database):
        self.database = database
```

- `Database` - это подключение к MongoDB
- `ObjectId` - в дальнейшем понадобится чтобы оборачивать id, будь то id пользователей или id постов

### 4. Добавляем первый метод для сохранения постов

Добавляем первый метод, которые записывает данные в базу данных.

```py
class PostRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_post(self, post: dict):
        payload = {
            "city": post["city"],
            "message": post["message"],
        }

        self.database["posts"].insert_one(payload)
```

### 5. Добавляем PostRepository в Service

Данный шаг требуется, чтобы наш репозиторий был доступен всем роутам модуля.

В `./app/posts/service.py` импортируем только что созданный класс `PostRepository`

```py
from .repository.repository import PostRepository
```

Теперь изменяем класс `Service` чтобы сохранял репозиторий себе.

```py
class Service:
    def __init__(self):
        self.repository = PostRepository(database)
```

### 6. Изменим логику в роуте чтобы сохранял в базу данных

Данный код не сохраняет пост в базу данных, но мы дополним чтобы сохранял.

```py
from app.utils import AppModel

from . import router


class CreatePostRequest(AppModel):
    city: str
    message: str


class CreatePostResponse(AppModel):
    message: str


@router.post("/", response_model=CreatePostResponse)
def create_post(
    req: CreatePostRequest,
):
    return {"message": "nFactorial School"}
```


Сначала импортируем сервис данного модуля:
```py
from fastapi import Depends

from ..service import Service, get_service
```

Изменяем аргумент модуля, чтобы имел доступ к сервису модуля:

```py
@router.post("/", response_model=CreatePostResponse)
def create_post(
    req: CreatePostRequest,
    svc: Service = Depends(get_service),
):
    return {"message": "nFactorial School"}
```

Передаем данные из запроса в функцию репозитория `create_post`, но перед этим сконвертируем данные в тип `dict`.

```py
@router.post("/", response_model=CreatePostResponse)
def create_post(
    req: CreatePostRequest,
    svc: Service = Depends(get_service),
):
    post = req.dict()
    svc.repository.create_post(post)
    return {"message": "nFactorial School"}
```

Все, на данном этапе данные сохраняются в базу данных.
