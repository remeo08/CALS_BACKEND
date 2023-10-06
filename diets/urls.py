from django.urls import path
from . import views

urlpatterns = [
    path("", views.DietView.as_view()),
]
