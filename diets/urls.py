from django.urls import path
from . import views

urlpatterns = [
    path("", views.DietView.as_view()),
    # path("quantity", views.QuantityView.as_view()),
    path("<int:pk>", views.PutDiet.as_view()),
    # path("meal/<int:pk>", views.SelectedDietDetail.as_view()),
]
