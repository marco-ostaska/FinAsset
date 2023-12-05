from django.urls import path
from . import views

urlpatterns = [
    path("projecao_low", views.projecao_low, name="projecaoLow")

]
