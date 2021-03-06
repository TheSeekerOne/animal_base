from datetime import date
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import get_user

from animals.forms import AnimalForm, ShowForm, AddForm
from animals.models import Animal
from animals.utils import get_data_by_id
from animals.decorators import groups_required


class IndexView(View):
    """Выводит информацию об API на главную страницу"""
    form_class = AddForm
    template_name = 'animals/index.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


class AnimalView(View):
    """Отображает страницу с выбором животного для дальнейших действий"""
    form_class = AnimalForm
    template_name = 'animals/animal.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        can_add = False
        if get_user(request).groups.filter(Q(name="user") | Q(name="admin")).count():
            can_add = True
        return render(request, self.template_name, {'form': form, "can_add": can_add})


class ShowAnimalView(View):
    """Показывает информацию о выбранном животном"""
    form_class = ShowForm
    template_name = 'animals/show.html'

    def post(self, request, *args, **kwargs):
        animal_id = int(request.POST.get("animals"))
        initial = get_data_by_id(animal_id)
        form = self.form_class(initial=initial)
        is_user = is_admin = False
        if get_user(request).groups.filter(name="user").count():
            is_user = True
        if get_user(request).groups.filter(name="admin").count():
            is_user = is_admin = True
        return render(request, self.template_name,
                      {'form': form,
                       "animal_id": animal_id,
                       "is_user": is_user,
                       "is_admin": is_admin,
                       }
                      )


@method_decorator(groups_required(names=("user", "admin")), name="dispatch")
class AddAnimalView(View):
    """Добавляет новое животное в БД"""
    form_class = AddForm
    template_name = "animals/add.html"

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            animal = Animal(
                name=form.cleaned_data.get("name"),
                age=form.cleaned_data.get("age"),

                weight=form.cleaned_data.get("weight"),
                height=form.cleaned_data.get("height"),
                spec_features=form.cleaned_data.get("spec_features")
            )
            arrival_date = form.cleaned_data.get("arrival_date")
            if arrival_date:
                animal.arrival_date = arrival_date
            animal.save()
            return HttpResponseRedirect(reverse('animals:animal'))
        else:
            return HttpResponse(status=400)


@method_decorator(groups_required(names=("user", "admin")), name="dispatch")
class EditAnimalView(View):
    """Редактирует животное имеющееся в БД"""
    form_class = AddForm
    template_name = "animals/edit.html"

    def dispatch(self, request, animal_id, *args, **kwargs):
        animal = Animal.objects.filter(pk=animal_id)
        if not len(list(animal)):
            return HttpResponse(status=404)
        return super().dispatch(request, animal_id, *args, **kwargs)

    def get(self, request, animal_id):
        initial = get_data_by_id(animal_id)
        form = self.form_class(initial=initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, animal_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            animal = Animal.objects.filter(pk=animal_id)
            arrival_date = form.cleaned_data.get("arrival_date") or timezone.now().date()
            animal.update(
                name=form.cleaned_data.get("name"),
                age=form.cleaned_data.get("age"),
                arrival_date=arrival_date,
                weight=form.cleaned_data.get("weight"),
                height=form.cleaned_data.get("height"),
                spec_features=form.cleaned_data.get("spec_features")
            )
            return HttpResponseRedirect(reverse('animals:animal'))
        else:
            return HttpResponse(status=400)


@method_decorator(groups_required(names=("admin",)), name="dispatch")
class DeleteAnimalView(View):
    """Производит "мягкое удаление" животного из БД"""
    def get(self, request, animal_id):
        animal = get_object_or_404(Animal, pk=animal_id)
        animal.delete()
        return HttpResponseRedirect(reverse('animals:animal'))
