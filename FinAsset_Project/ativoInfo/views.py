from django.shortcuts import render
from .forms import Info
from custom import ativos_info
# Create your views here.

def info_form(request):
    if request.method == "POST":
        form = Info(request.POST) 
        if form.is_valid():
           results = ativos_info.retorna(form.cleaned_data['opt'], form.cleaned_data['ticker'].splitlines())
           sorted_results = sorted(results, key=lambda x: x['desconto'],reverse=True)
           return render(request, "info.html", {"form": form, 
                                                      "results": results,
                                                      "sorted_results": sorted_results})
        
        
    form = Info()
    return render(request, "info.html", {"form": form})
       
           