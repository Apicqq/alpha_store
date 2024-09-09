# Интернет-магазин — Тестовое задание

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)


## Ключевые возможности сервиса
### Админ-панель:
- Просмотр, редактирование, удаление продуктов
- Просмотр, редактирование, удаление категорий
- Просмотр, редактирование, удаление подкатегорий

### API:
- Аутентификация с помощью токенов (библиотека djoser)
- Просмотр списка продуктов, категорий, подкатегорий
- Добавление, удаление продуктов в/из корзины. Изменение количества
- Просмотр содержимого корзины


В текущей реализации проект использует базу данных SQLite, но при необходимости можно без проблем перейти и на боевой вариант, например, MySQL либо Postgres.

## Использованные при реализации проекта технологии
 - Python 3.11
 - Django
 - DRF
 - drf-yasg

## Как установить проект

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Apicqq/alpha_store
```

```
cd <путь_до_папки_с_проектом>/alpha_store
```

Установить зависимости проекта:

* Если у вас установлен Poetry:
    ```
    poetry install
    ```
* Либо через стандартный менеджер зависимостей pip:
    
  Создайте виртуальное окружение:

    ```
    python3 -m venv venv
    ```
  Активируйте его:

    * Если у вас Linux/macOS
    
        ```
        source venv/bin/activate
        ```
    
    * Если у вас windows
    
        ```
        source venv/scripts/activate
        ```
    
        ```
        python3 -m pip install --upgrade pip
        ```
  И установите зависимости:
    ```
    pip install -r requirements.txt
    ```

Применить миграции:
```
python alpha_store/manage.py migrate
```

Запустить проект (в зависимости от выбранного менеджера зависимости) можно командами:
- `poetry run python alpha_store/manage.py runserver`
- `python alpha_store/manage.py runserver`

### Документация

Для проекта реализована API-документация.

После запуска приложения она будет доступна по адресам:

Для документации Swagger:

[http://127.0.0.1:8000/api/swagger/](http://127.0.0.1:8000/api/swagger/)


Для документации ReDoc:

[http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/)
## Автор проекта

[Никита Смыков](https://github.com/Apicqq)


