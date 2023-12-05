# Create your views here.
from django.shortcuts import render
from .forms import Formulario
from custom import projecao_preco_low

# Create your views here.

def projecao_low(request):
    if request.method == "POST":
        form = Formulario(request.POST)
        if form.is_valid():
            ticker_list = form.cleaned_data['ticker'].splitlines()
            ativos = projecao_preco_low.retorna(ticker_list)
            print("------------------>", ativos)
            return render(request, "projecao_low.html", {"form": form, "ativos": ativos})

    form = Formulario()
    return render(request, "projecao_low.html", {"form": form})


