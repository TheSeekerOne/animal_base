from django.urls import path
from . import views


app_name = 'animals'

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('show/', views.ShowAnimalView.as_view()),
    path('add/', views.AddAnimalView.as_view()),
    path('edit/<int:animal_id>', views.EditAnimalView.as_view()),
    path('delete/<int:animal_id>', views.DeleteAnimalView.as_view()),
]
