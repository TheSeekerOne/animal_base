from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        view_animal = Permission.objects.get(codename="view_animal")
        add_animal = Permission.objects.get(codename="add_animal")
        change_animal = Permission.objects.get(codename="change_animal")
        delete_animal = Permission.objects.get(codename="delete_animal")

        guest = Group.objects.create(name="guest")
        guest.permissions.add(view_animal)

        user = Group.objects.create(name="user")
        [user.permissions.add(perm) for perm in (view_animal, add_animal, change_animal)]

        admin = Group.objects.create(name="admin")
        [admin.permissions.add(perm) for perm in (view_animal, add_animal, change_animal, delete_animal)]
