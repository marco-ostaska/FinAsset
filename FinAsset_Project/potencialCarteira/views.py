from django.shortcuts import render
from .forms import Formulario
from custom import potencial_carteira
from django.views.decorators.cache import never_cache
# Create your views here.


@never_cache
def info_form(request):
    if request.method == "POST":
        form = Formulario(request.POST) 
        if form.is_valid():
            tickers = form.cleaned_data['ticker'].splitlines()
            pesos = form.cleaned_data['peso'].splitlines()
            carteira = potencial_carteira.retorna(tickers, pesos)
            # Extrair pares de ticker e peso e convertê-los em uma lista de tuplas
            ticker_list = [(ticker, peso) for ticker_info in carteira['Tickers'] for ticker, peso in ticker_info.items()]

                # Ordenar a lista de tuplas com base nos pesos, em ordem decrescente
            sorted_tickers = sorted(ticker_list, key=lambda x: x[1], reverse=True)

            # Substituir a lista original de tickers pela lista ordenada
            carteira['SortedTickers'] = sorted_tickers



            return render(request, "potencial_carteira.html", {"form": form, "carteira": carteira})
        
        
    form = Formulario()
    return render(request, "potencial_carteira.html", {"form": form})
       



