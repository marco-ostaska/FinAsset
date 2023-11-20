from django.shortcuts import render
from .forms import Formulario
from custom import monte_carlo
# Create your views here.

def info_form(request):
    if request.method == "POST":
        form = Formulario(request.POST) 
        if form.is_valid():
           carteiras = monte_carlo.retorna(form.cleaned_data['ticker'].splitlines())

           return render(request, "monte_carlo.html", {"form": form, "carteiras": carteiras})
        
        
    form = Formulario()
    return render(request, "monte_carlo.html", {"form": form})
       
           