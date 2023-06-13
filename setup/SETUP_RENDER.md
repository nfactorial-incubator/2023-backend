# Deploy

Для деплоя нашего API мы воспользуемся двумя сервисами:

- [mongodb.com](https://www.mongodb.com/)
- [render.com](https://render.com/)

## Настройка MongoDB

## 01. Зайдем на страницу [mongodb.com](https://www.mongodb.com/)

Нажмите на "Start Free"

![img](./resources/01.png)

## 02. Пройдем регистрацию

![img](./resources/02.png)

## 03. Создадим базу данных

![img](./resources/04.png)

## 04. Выбираем правильные параметры

Убидидетесь что выбрали именно эти параметры

![img](./resources/06.png)

## 05. Заполняем логин и пароль для подключения к Mongo

Запомните логин и пароль, он позже понадобится!

Далее нажимаем "Create User"

![img](./resources/07.png)

## 06. Настроим сеть чтобы смогли подключаться

Выбираем меню "Network Access"

![img](./resources/10.png)

## 07. Заполняем IP адрес

- `0.0.0.0/0`
- `All`

![img](./resources/11.png)

## 08. Переходим в меню "Database"

![img](./resources/112.png)

## 09. Запоминаем URL для подключения

Данный URL позже понадобится, для каждой базы он уникальный.

![img](./resources/12.png)

## Настройка Репозитория

## 01. Сделаем форк стартер кода

![img](./resources/13.png)

## 02. Указываем данные

![img](./resources/14.png)

## 03. Ждем

![img](./resources/15.png)

## 04. Успешно создался

![img](./resources/16.png)

## Настройка Render.com

## 01. Заходим на [render.com](https://render.com/)

![img](./resources/18.png)

## 02. Регистрируемся

![img](./resources/19.png)

## 03. Выбираем "New Blueprint"

![img](./resources/20.png)

## 04. Выбираем "Configure Account"

![img](./resources/21.png)

## 05. Выбираем свой аккаунт куда ранее сделали форк

![img](./resources/22.png)

## 06. Даем разрешения

![img](./resources/23.png)

## 07. Выбираем наш репозиторий

![img](./resources/24.png)

## 07. Вводим данные

В нижнее поле `MONGO_URL` вводим ссылку для подключения которую запомнили в [этом шаге](#09-запоминаем-url-для-подключения).

Ссылка для подключения будет такого вида, вам нужно подставить пароль вместо `<password>`.

> Если репозиторий не подтягивается, то значит что в репозиторий отсутствует файл `render.yaml`. Без него данный пункт не будет работать.

```
mongodb+srv://admin:<password>@cluster0.eyube5m.mongodb.net/?retryWrites=true&w=majority
```

![img](./resources/26.png)

## 08. Нажимаем "Apply"

![img](./resources/27.png)

## 09. Ждем

![img](./resources/28.png)

## 10. Создался!

![img](./resources/29.png)

## 10. Переходим в "Dashboard" и выбираем наш сервис

![img](./resources/30.png)

## 11. Наш API задеплоем и имеет свой URL

Настроен автоматическое развертывание на сервер.

![img](./resources/31.png)
