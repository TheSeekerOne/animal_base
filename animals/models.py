from datetime import date
from django.db import models
from django.db.models.query import QuerySet
from django.utils import timezone


class SoftDeletionQuerySet(QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(deleted_at=timezone.now())

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


class SoftDeletionManager(models.Manager):
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
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
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
        return f"{self.name} {self.age} {self.arrival_date}"
