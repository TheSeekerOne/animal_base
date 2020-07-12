![](https://img.shields.io/static/v1?label=Python&message=3.7&color=blue)
# animal_base
Интерфейс управления базой данных информации о животных для приютов.

## Документация

#### Установка зависимостей
    $ pip install -r requirements.txt
#### Миграция моделей БД    
    $ python manage.py migrate
    $ python manage.py makemigrations animals
    $ python manage.py migrate
#### Создание администратора
    $ python manage.py createsuperuser
#### Создание групп для пользователей
    $ python manage.py create_groups
#### Запуск
    $ python manage.py runserver

### Структура проекта

В корне  по адресу "/" расположена страница с описанием API и интерактивными примерами.<br>
По адрес "/admin/" расположена административная панель.<br>
По адресу "/animals/" расположена страница выбора животного с кнопками выбора животного / добавления нового животного(для групп user, admin).<br>


