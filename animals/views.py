from django.shortcuts import render
from django.views import View


class IndexView(View):
    """Выводит информацию об API на главную страницу"""

    def get(self, request, *args, **kwargs):
        return render(request, "animals/index.html")


class ShowAnimalView(View):
    """Показывает информацию о выбранном животном"""
    pass


class AddAnimalView(View):
    """Добавляет новое животное в БД"""
    pass


class EditAnimalView(View):
    """Редактирует животное имеющееся в БД"""
    pass


class DeleteAnimalView(View):
    """Производит "мягкое удаление" животного из БД"""
    pass
