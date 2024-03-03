from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('input', views.input_page, name='input_page'),
]
