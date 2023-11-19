from django.shortcuts import render
from .forms import Formulario
from custom import projecao_preco_ativos

# Create your views here.

def projecao_precos(request):
    if request.method == "POST":
        form = Formulario(request.POST) 
        if form.is_valid():
            ticker_list = form.cleaned_data['ticker'].splitlines()
            results = projecao_preco_ativos.retorna(ticker_list)
            print(results)
            return render(request, "projecao_preco.html", {"form": form, "results": results})   

    form = Formulario()
    return render(request, "projecao_preco.html", {"form": form})


       