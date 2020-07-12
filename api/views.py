from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from animals.decorators import basicauth, groups_required
from animals.forms import AddForm
from animals.models import Animal


class AnimalView(View):
    def get(self, request, animal_id=None):
        if animal_id is None:
            animals = list(Animal.objects.values())
            return JsonResponse(animals, safe=False, status=200)
        else:
            animal = get_object_or_404(Animal, pk=animal_id)
            animal = model_to_dict(animal)
            return JsonResponse(animal, status=200)


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(basicauth, name="dispatch")
@method_decorator(groups_required(names=("user", "admin")), name="dispatch")
class AddAnimalView(View):
    form_class = AddForm

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
            return JsonResponse({"id": animal.id}, status=201)
        else:
            return HttpResponse(status=400)


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(basicauth, name="dispatch")
@method_decorator(groups_required(names=("user", "admin")), name="dispatch")
class EditAnimalView(View):
    form_class = AddForm

    def post(self, request, animal_id):
        form = self.form_class(request.POST)
        if form.is_valid():
            animal = Animal.objects.filter(pk=animal_id)
            if not len(list(animal)):
                return HttpResponse(status=404)
            arrival_date = form.cleaned_data.get("arrival_date") or timezone.now().date()
            animal.update(
                name=form.cleaned_data.get("name"),
                age=form.cleaned_data.get("age"),
                arrival_date=arrival_date,
                weight=form.cleaned_data.get("weight"),
                height=form.cleaned_data.get("height"),
                spec_features=form.cleaned_data.get("spec_features")
            )
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=400)


@method_decorator(csrf_exempt, name="dispatch")
@method_decorator(basicauth, name="dispatch")
@method_decorator(groups_required(names=("admin",)), name="dispatch")
class DeleteAnimalView(View):
    def delete(self, request, animal_id):
        animal = get_object_or_404(Animal, pk=animal_id)
        animal.delete()
        return HttpResponse(status=200)
