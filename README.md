# YaMDb api финальный проект спринта 10
Проект YaMDb собирает отзывы пользователей на произведения.

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
 git clone git@github.com:Ilyako78/api_final_yatube.git 
 cd api_final_yatube
``` 

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
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

## Примеры
Полная спецификация api
```
/redoc/
```

Запрос кода подтверждения при регистрации
```
/api/v1/auth/signup/
```

Получение JWT-токена
```
/api/v1/auth/token/
```

Получение списка всех категорий
```
/api/v1/categories/
```

Получение списка всех произведений
```
/api/v1/titles/
```

Загрузить данные из csv файлов:
```
python3 manage.py upload_db
```
