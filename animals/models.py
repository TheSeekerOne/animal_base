from django.db import models
from datetime import date


class Animal(models.Model):
    """Модель животного находящегося в приюте"""
    name = models.CharField(max_length=40)
    age = models.IntegerField()
    arrival_date = models.DateField(default=date.today)
    weight = models.DecimalField(max_digits=5, decimal_places=1)
    height = models.DecimalField(max_digits=4, decimal_places=2)
    spec_features = models.TextField()
    deleted = models.BooleanField(default=False)
