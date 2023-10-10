from django.urls import path
from . import views

urlpatterns = [
    path("", views.DietView.as_view()),
    path("review/", views.ReviewView.as_view()),
]
