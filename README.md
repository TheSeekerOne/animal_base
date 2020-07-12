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

+ В корне  по адресу "/" расположена страница с описанием API и интерактивными примерами.
+ По адрес "/admin/" расположена административная панель.
+ По адресу "/animals/" расположена страница выбора животного с кнопками:
  + выбора животного(для всех групп)
  + добавления нового животного(для групп user, admin)
+ По адресу "/animals/show/" - страница просмотра выбранного животного с кнопками:
  + редактирования животного(для групп user, admin)
  + удаления животного(для группы admin)
+ По адресу "/animals/add/" - форма добавления нового животного
+ По адресу "/animals/edit/{ID}" - форма редактирования информации о животном
+ По адресу "/users/login/" - форма авторизации пользователя
+ По адресу "/users/register" - форма регистрации пользователя

### Структура прав пользователей
Права доступа назначаются пользователям через группы в административной панель главным администратором
+ Группы:
  + guest
    + чтение
  + user
    + чтение
    + добавление
    + изменение
  + admin
    + чтение
    + добавление
    + изменение
    + мягкое удаление
    
### Структура API
+ GET "/api/animal/"
  + ->  code 200, json список всех животных
+ GET "/api/animal/{ID}" 
  + -> code 200, вернет json словарь с данными на питомца
  + -> code 404, если ID питомца нет в БД
+ POST "/api/animal/add/", данные в виде: application/x-www-form-urlencoded, заголовок авторизации: Request header: "Authorization: Basic {base64 login:password}"
  + -> code 201, вернет json словарь {"id": id} c ID нового питомца
  + -> code 400, если ошибка валидации
+ POST "/api/animal/{ID}/edit/", данные в виде: application/x-www-form-urlencoded, заголовок авторизации: Request header: "Authorization: Basic {base64 login:password}"
  + -> code 200
  + -> code 400, если ошибка валидации
  + -> code 404, если ID питомца нет в БД
+ DELETE "/apianimal/{ID}/delete/"  
  + -> code 200
  + -> code 404, если ID питомца нет в БД
