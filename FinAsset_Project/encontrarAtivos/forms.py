from django import forms

class Info(forms.Form):
    opt = forms.ChoiceField(
        choices=[
            (1, 'IBOV'),
            (2, 'IDIV'),
            (3, 'Small Caps'),
            (4, 'IFIX')
        ], widget=forms.RadioSelect
    )


    
