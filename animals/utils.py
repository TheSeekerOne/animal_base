from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied

from animals.models import Animal


def get_data_by_id(animal_id):
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


def groups_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None, names=None):
    def check_user_groups(user):
        if names:
            if not any(map(lambda name: user.groups.filter(name=name).count(), names)):
                raise PermissionDenied
        return True

    actual_decorator = user_passes_test(
        check_user_groups,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

