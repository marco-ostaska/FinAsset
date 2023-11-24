from django import forms

class Info(forms.Form):
    opt = forms.ChoiceField(
        choices=[
            (1, 'IBOV'),
            (2, 'IDIV'),
            (3, 'Small Caps'),
            (4, 'IFIX'),
            (5, 'Saneamento'),
            (6, 'Eletrica'),
            (7, 'Bancos'),
            (8, 'Seguros'),
            (9, 'Saude'),
        ], widget=forms.Select
    )



