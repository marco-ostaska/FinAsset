from django import forms

class Formulario(forms.Form):
    ticker = forms.CharField(widget=forms.Textarea)
    peso = forms.CharField(widget=forms.Textarea)