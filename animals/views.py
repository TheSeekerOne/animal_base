from datetime import date
from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render
from django.views import View
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from animals.forms import IndexForm, ShowForm, AddForm
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
    form_class = AddForm
    template_name = "animals/add.html"

    @method_decorator(login_required)
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        data = request.POST
        form = self.form_class(request.POST)
        arrival_date = date(int(data.get("arrival_date_year")), int(data.get("arrival_date_month")), int(data.get("arrival_date_day")))
        if form.is_valid():
            animal = Animal.objects.create(
                name=data.get("name"),
                age=data.get("age"),
                arrival_date=arrival_date,
                weight=data.get("weight"),
                height=data.get("height"),
                spec_features=data.get("spec_features")
            )
        return HttpResponseRedirect(reverse('animals:index'))


class EditAnimalView(View):
    """Редактирует животное имеющееся в БД"""
    pass


class DeleteAnimalView(View):
    """Производит "мягкое удаление" животного из БД"""
    pass
