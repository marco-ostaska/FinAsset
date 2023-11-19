from django.urls import path
from . import views

urlpatterns = [
    path("projecao_precos", views.projecao_precos, name="projecaoPrecos")

]