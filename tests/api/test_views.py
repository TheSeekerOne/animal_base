import base64
import random
from datetime import date, datetime
from decimal import Decimal

import pytest

from django.contrib.auth.models import User, Group, Permission
from animals.models import Animal

import factory
import factory.fuzzy


#  fabrics --------------------------------------------------------------------
class AnimalFactory(factory.django.DjangoModelFactory):

    name = factory.Sequence(lambda n: 'Тестовое животное №{}'.format(n))
    age = factory.fuzzy.FuzzyInteger(1, 150)
    arrival_date = factory.fuzzy.FuzzyDate(date(2020, 1, 1))
    weight = factory.fuzzy.FuzzyDecimal(low=0, high=9999, precision=1)
    height = factory.fuzzy.FuzzyDecimal(low=0, high=99, precision=2)
    spec_features = factory.fuzzy.FuzzyText()

    class Meta:
        model = 'animals.Animal'


#  fixtures -------------------------------------------------------------------
@pytest.fixture()
def data():
    data = {
        'name': 'Пёс Джона Уика',
        'age': 6,
        'arrival_date': '2020-04-03',
        'weight': 32.5,
        'height': 0.5,
        'spec_features': 'Хороший пёсик',
    }
    return data


@pytest.fixture()
def animals(db):
    """создает в базе данных записи о 10 животных"""
    AnimalFactory.reset_sequence()
    for i in range(10):
        AnimalFactory()


@pytest.fixture()
def guest_group(db):
    view_animal = Permission.objects.get(codename="view_animal")
    guest = Group.objects.create(name="guest")
    guest.permissions.add(view_animal)
    return guest


@pytest.fixture()
def user_group(db):
    view_animal = Permission.objects.get(codename="view_animal")
    add_animal = Permission.objects.get(codename="add_animal")
    change_animal = Permission.objects.get(codename="change_animal")
    user = Group.objects.create(name="user")
    [user.permissions.add(perm) for perm in (view_animal, add_animal, change_animal)]
    return user


@pytest.fixture()
def admin_group(db):
    view_animal = Permission.objects.get(codename="view_animal")
    add_animal = Permission.objects.get(codename="add_animal")
    change_animal = Permission.objects.get(codename="change_animal")
    delete_animal = Permission.objects.get(codename="delete_animal")
    admin = Group.objects.create(name="admin")
    [admin.permissions.add(perm) for perm in (view_animal, add_animal, change_animal, delete_animal)]
    return admin


@pytest.fixture()
def guest_token(db, guest_group):
    user = User.objects.create_user(
        'guest', password='guestguest', is_staff=True
    )
    user.groups.add(guest_group)
    user.save()
    token = base64.b64encode('guest:guestguest'.encode('utf-8'))
    return token.decode('ascii')


@pytest.fixture()
def user_token(db, user_group):
    user = User.objects.create_user(
        'user', password='useruser', is_staff=True
    )
    user.groups.add(user_group)
    token = base64.b64encode('user:useruser'.encode('utf-8'))
    return token.decode('ascii')


@pytest.fixture()
def admin_token(db, admin_group):
    user = User.objects.create_user(
        'admin', password='adminadmin', is_staff=True
    )
    user.groups.add(admin_group)
    user.save()
    token = base64.b64encode('admin:adminadmin'.encode('utf-8'))
    return token.decode('ascii')


def test_get_all_animals(animals, client):
    """get запрос на /api/animal/ возвращает код 200 и список словарей с данными о животных"""

    url_template = '/api/animal/'
    total = len(Animal.objects.all())
    animals = list(Animal.objects.values())

    response = client.get(url_template)
    assert response.status_code == 200
    assert len(response.json()) == total
    # assert response.json() == animals # TODO("Добавить конвертацию 'arrival_date': '2020-04-29'
    #  в  datetime.date(2020
    # , 4, 29) weight, height to Decimal() ")


def test_get_animal_id_200(animals, client):
    """get запрос на /api/animal/{id} возвращает код ответа 200, если питомец с id
    существует в базе данных"""

    url_template = '/api/animal/{}/'
    total = len(Animal.objects.all())

    for animal in Animal.objects.all():
        url = url_template.format(animal.id)
        response = client.get(url)
        assert response.status_code == 200
        assert len(Animal.objects.all()) == total


def test_get_animal_id_404(animals, client):
    """get запрос на /api/animal/{id} возвращает код ответа 404, если питомец с id
    отсутствует в базе данных"""

    url_template = '/api/animal/{}/'
    key = random.randint(10000, 100_000)

    response = client.get(url_template.format(key))
    assert response.status_code == 404


def test_get_animal_data(animals, client):
    """get запрос на /api/animal/{id} возвращает верные типы и значения из базы данных"""

    url_template = '/api/animal/{}/'

    for animal in Animal.objects.all():
        response = client.get(url_template.format(animal.id))
        content = response.json()
        assert isinstance(content.get('id'), int)
        assert content.get('id') == animal.id

        assert isinstance(content.get('name'), str)
        assert content.get('name') == animal.name

        assert isinstance(content.get('age'), int)
        assert content.get('age') == animal.age

        assert isinstance(content.get('arrival_date'), str)
        assert datetime.strptime(content.get('arrival_date'), "%Y-%m-%d").date() == animal.arrival_date

        assert isinstance(content.get('weight'), str)
        assert Decimal(content.get('weight')) == animal.weight

        assert isinstance(content.get('height'), str)
        assert Decimal(content.get('height')) == animal.height

        assert isinstance(content.get('spec_features'), str)
        assert content.get('spec_features') == animal.spec_features


@pytest.mark.django_db(transaction=True)
def test_add_animal_by_user(client, user_token, data):
    """post запрос на /api/animal/add/ с пользовательскими правами вернет код 201,
     объект json {'id': id} и создаст объект в базе"""
    url_template = '/api/animal/add/'
    response = client.post(
        url_template,
        data=data,
        HTTP_AUTHORIZATION=f'Basic {user_token}'
    )
    assert response.status_code == 201
    document = response.json()
    # Объект был сохранен в базу
    animal = Animal.objects.get(pk=document['id'])
    assert animal.name == 'Пёс Джона Уика'
    assert animal.age == 6
    assert animal.arrival_date == datetime.strptime('2020-04-03', "%Y-%m-%d").date()
    assert animal.weight == Decimal("32.5")
    assert animal.height == Decimal("0.5")
    assert animal.spec_features == 'Хороший пёсик'


@pytest.mark.django_db(transaction=True)
def test_add_animal_by_admin(client, admin_token, data):
    """post запрос на /api/animal/add/ с администраторскими правами вернет код 201,
     объект json {'id': id} и создаст объект в базе"""
    url_template = '/api/animal/add/'
    response = client.post(
        url_template,
        data=data,
        HTTP_AUTHORIZATION=f'Basic {admin_token}'
    )
    assert response.status_code == 201
    document = response.json()
    # Объект был сохранен в базу
    animal = Animal.objects.get(pk=document['id'])
    assert animal.name == 'Пёс Джона Уика'
    assert animal.age == 6
    assert animal.arrival_date == datetime.strptime('2020-04-03', "%Y-%m-%d").date()
    assert animal.weight == Decimal("32.5")
    assert animal.height == Decimal("0.5")
    assert animal.spec_features == 'Хороший пёсик'


@pytest.mark.django_db(transaction=True)
def test_add_animal_mo_head(client, data):
    """post запрос на /api/animal/add/ без Authorization header вернет 401"""
    url_template = '/api/animal/add/'
    response = client.post(
        url_template,
        data=data
    )
    assert response.status_code == 401


@pytest.mark.django_db(transaction=True)
def test_add_animal_by_guest(client, guest_token, data):
    """post запрос на /api/animal/add/ с гостевыми правами вернет 403"""
    url_template = '/api/animal/add/'
    response = client.post(
        url_template,
        data=data,
        HTTP_AUTHORIZATION=f'Basic {guest_token}'
    )
    assert response.status_code == 403


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize('field', [
        'name', 'age', 'weight', 'height',
    ])
def test_invalid_add_animal(client, admin_token, data, field):
    """post запрос на /api/animal/add/ с невалидными данными вернет код 400"""
    url_template = '/api/animal/add/'
    del(data[field])
    response = client.post(
        url_template,
        data=data,
        HTTP_AUTHORIZATION=f'Basic {admin_token}'
    )
    assert response.status_code == 400
