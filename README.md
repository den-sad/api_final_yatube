### Проект API для социальной сети Yatube:

Данный проект предназначен для обеспечения доступа к серверной части через запросы API
Доступ обсепечивается к данным постов, групп, комментариев и подпискам пользователей

Осуществяется контроль и разделение доступа по пользователям с использованием JWT токенов

### Доступные END-поинты:

Описание END-поинтов и формата данных в формате REDOC

```
http://127.0.0.1:8000/redoc/
```

Авторизация и аутентификация:

```
http://127.0.0.1:8000/api/v1/jwt/
```

Работа с постами:

```
http://127.0.0.1:8000/api/v1/posts/

```

Работа с группами:
Только просмотр

```
http://127.0.0.1:8000/api/v1/groups/
```

Добавление осуществляется из административной части сайта

```
http://127.0.0.1:8000/admin/
```

Работа с комментариями:

```
http://127.0.0.1:8000/api/v1/posts/{id}/comments/
```

Работа с подписками:

```
http://127.0.0.1:8000/api/v1/follow/
```

### Примеры

Получение списка постов

```
Запрос GET http://127.0.0.1:8000/api/v1/posts/
Ответ {
        "count": 123,
        "next": "http://api.example.org/accounts/?offset=400&limit=100",
        "previous": "http://api.example.org/accounts/?offset=200&limit=100",
        "results": [
            {}
        ]
    }
```

Создание новго поста

```
Запрос POST http://127.0.0.1:8000/api/v1/posts/
    {
        "text": "Текст поста",
        "image": "",
        "group": 0
    }

Ответ
    {
        "id": 0,
        "author": "Username автора",
        "text": "Текст поста",
        "pub_date": "2019-08-24T14:15:22Z",
        "image": Null,
        "group": 0
    }
```

Комментрируем пост 2

```
    Запрос POST http://127.0.0.1:8000/api/v1/posts/2/comments/
        {
            "text": "Комментарий к посту 2"
        }
    Ответ
        {
            "id": 0,
            "author": "Username автора",
            "text": "Комментарий к посту 2",
            "created": "2019-08-24T14:15:22Z",
            "post": 2
        }
```

Получение списка подписок пользователя

```
    Запрос GET http://127.0.0.1:8000/api/v1/follow/
    Ответ
        [
            {
                "user": "Username пользователя",
                "following": "Username автора"
            }
        ]
    Оформление подписки
    Запрос POST http://127.0.0.1:8000/api/v1/follow/
        {
            "following": "Username автора"
        }
    Ответ
        {
            "user": "Username пользователя",
            "following": "Username автора"
        }
```

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com:den-sad/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

Создание суперпользователя:

```
python3 manage.py createsuperuser
```

### Автор API Сатчин Дениc
