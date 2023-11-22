from django.urls import path
from . import views

urlpatterns = [
    path("encontrar", views.info_form, name="encontrarAtivo")

]