from django.urls import path
from . import views

urlpatterns = [
    path('clone_data/', views.clone_data),
]