from django.urls import path
from . import views

urlpatterns = [
    path("monte_carlo", views.info_form, name="monteCarlo")

]