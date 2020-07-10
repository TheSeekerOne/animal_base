from django.urls import path
from . import views


app_name = 'api'

urlpatterns = [
    path('animal/', views.AnimalView.as_view()),
    path('animal/<int:animal_id>/', views.AnimalView.as_view()),
    path('animal/add/', views.AddAnimalView.as_view()),
    path('animal/<int:animal_id>/edit/', views.EditAnimalView.as_view()),
    path('animal/<int:animal_id>/delete/', views.DeleteAnimalView.as_view()),
]
