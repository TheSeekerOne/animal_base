from datetime import date
from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone


class SoftDeletionQuerySet(QuerySet):
    """QuerySet определяющий поведение при удалении объекта"""

    def delete(self):
        """Подменяет вызов delete на update и изменяет параметр deleted_at"""
        return super(SoftDeletionQuerySet, self).update(deleted_at=timezone.now())

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        """Возвращает все неудаленные объекты"""
        return self.filter(deleted_at=None)

    def dead(self):
        """Возвращает все удаленные объекты"""
        return self.exclude(deleted_at=None)


class SoftDeletionManager(models.Manager):
    """Менеджер для мягкого удаления объектов"""
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class SoftDeletionModel(models.Model):
    """Базовый класс для определения моделей с возможностью 'мягкого удаления'
    для обращения ко всем объектам влючая удаленные
    использовать атрибут all_objects"""
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        """
        Метод реализующий мягкое удаление
        :return:
        """
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        """
        Метод реализующий классическое удаление, если потребуется удалить объект окончательно
        :return:
        """
        super(SoftDeletionModel, self).delete()


class Animal(SoftDeletionModel):
    """Модель животного находящегося в приюте"""
    name = models.CharField(max_length=40)
    age = models.IntegerField()
    arrival_date = models.DateField(default=date.today)
    weight = models.DecimalField(max_digits=5, decimal_places=1)
    height = models.DecimalField(max_digits=4, decimal_places=2)
    spec_features = models.TextField()

    def __str__(self):
        return f"Имя: {self.name}, возвраст: {self.age}, прибыл: {self.arrival_date}"
