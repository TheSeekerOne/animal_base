from django.core.exceptions import ObjectDoesNotExist
from animals.models import Animal


def get_data_by_id(animal_id):
    """
    Возвращает словарь с данными для заполнения формы информации о животном
    :param animal_id: int() ID животного из БД
    :return: initial_data: Dict() словарь для заполнения формы
    """
    try:
        animal = Animal.objects.get(pk=animal_id)
        initial_data = {
            "name": animal.name,
            "age": animal.age,
            "arrival_date": animal.arrival_date,
            "weight": animal.weight,
            "height": animal.height,
            "spec_features": animal.spec_features,
        }
    except ObjectDoesNotExist:
        initial_data = {}
    finally:
        return initial_data
