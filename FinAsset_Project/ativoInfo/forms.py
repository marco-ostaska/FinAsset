from django import forms

class Info(forms.Form):
    opt = forms.ChoiceField(
        choices=[
            (1, 'Ações'),
            (2, 'FII'),
        ], widget=forms.RadioSelect
    )
    ticker = forms.CharField(widget=forms.Textarea)

    
