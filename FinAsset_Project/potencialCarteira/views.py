from django.shortcuts import render
from .forms import Formulario
from custom import potencial_carteira
# Create your views here.

def info_form(request):
    if request.method == "POST":
        form = Formulario(request.POST) 
        if form.is_valid():
            tickers = form.cleaned_data['ticker'].splitlines()
            pesos = form.cleaned_data['peso'].splitlines()
            carteira = potencial_carteira.retorna(tickers, pesos)

            return render(request, "potencial_carteira.html", {"form": form, "carteira": carteira})
        
        
    form = Formulario()
    return render(request, "potencial_carteira.html", {"form": form})
       
           