from django.urls import path
from . import views

urlpatterns = [
    path("potencial_carteira", views.info_form, name="PotencialCarteira")

]