from django.shortcuts import render
from .forms import Info
from custom import encontrar_ativos
# Create your views here.

def info_form(request):
    if request.method == "POST":
        form = Info(request.POST) 
        if form.is_valid():
           results = encontrar_ativos.retorna(form.cleaned_data['opt'])
           print(results)
           return render(request, "encontrar.html", {"form": form, 
                                                      "results": results})
        
        
    form = Info()
    return render(request, "encontrar.html", {"form": form})
       
           