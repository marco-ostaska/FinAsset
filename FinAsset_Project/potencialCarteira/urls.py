from django.urls import path
from . import views

urlpatterns = [
    path("potencial", views.info_form, name="PotencialCarteira")

]
