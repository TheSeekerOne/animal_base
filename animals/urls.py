from django.urls import path
from . import views


app_name = 'animals'

urlpatterns = [
    path('', views.AnimalView.as_view(), name="animal"),
    path('show/', views.ShowAnimalView.as_view()),
    path('add/', views.AddAnimalView.as_view()),
    path('edit/<int:animal_id>', views.EditAnimalView.as_view()),
    path('delete/<int:animal_id>', views.DeleteAnimalView.as_view()),
]
