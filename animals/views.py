from django.http import HttpResponse

from django.shortcuts import render
from django.views import View

from animals.forms import IndexForm, ShowForm
from animals.models import Animal


class IndexView(View):
    """Выводит информацию об API на главную страницу"""
    form_class = IndexForm
    template_name = 'animals/index.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


class ShowAnimalView(View):
    """Показывает информацию о выбранном животном"""
    form_class = ShowForm
    template_name = 'animals/show.html'

    def post(self, request, *args, **kwargs):
        animal_id = int(request.POST.get("animals"))
        animal = Animal.objects.get(pk=animal_id)
        initial = {
            "name": animal.name,
            "age": animal.age,
            "arrival_date": animal.arrival_date,
            "weight": animal.weight,
            "height": animal.height,
            "spec_features": animal.spec_features,
        }
        form = self.form_class(initial=initial)
        return render(request, self.template_name, {'form': form, "animal_id": animal_id})


class AddAnimalView(View):
    """Добавляет новое животное в БД"""
    pass


class EditAnimalView(View):
    """Редактирует животное имеющееся в БД"""
    pass


class DeleteAnimalView(View):
    """Производит "мягкое удаление" животного из БД"""
    pass
