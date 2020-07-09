from django.urls import path
from . import views


app_name = 'animals'

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('show/', views.ShowAnimalView.as_view()),
    path('add/', views.AddAnimalView.as_view()),
    path('edit/', views.EditAnimalView.as_view()),
    path('delete/', views.DeleteAnimalView.as_view()),
]
