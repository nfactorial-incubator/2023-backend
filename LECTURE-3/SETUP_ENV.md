# Настройка переменных окружения

## 1. Создание .env

В корневой папке проекта создайте `.env` файл со следующим содержимым:

```
AWS_ACCESS_KEY_ID=key
AWS_SECRET_ACCESS_KEY=secret
```

Вместо key и secret поставьте свои значения.

## 2. Подключение .env к docker-compose

Добавьте указанную линию docker-compose.yml

```yaml
app:
  build:
    context: .
    dockerfile: ./deploy/dockerfiles/Dockerfile
  environment:
    - MONGOHOST=mongodb
  env_file: .env # <--------- Добавить эту линию к сервису `app`
  volumes:
    - ./:/code
  ports:
    - "8000:8000"
  depends_on:
    - mongodb
```

> Если же вы запускаете API не с докера, а напрямую то можете выполнить след. операцию чтобы подтянуть переменные `export $(cat .env)`

---

В render.com и railway.app вам тоже нужно будет добавить данные переменные окружения.

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
