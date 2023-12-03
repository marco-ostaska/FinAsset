from django import forms

class Info(forms.Form):
    opt = forms.ChoiceField(
        choices=[
            (1, 'IBOV'),
            (2, 'IDIV'),
            (3, 'Small Caps'),
            (4, 'IFIX'),
            (5, 'IBRX50'),
            (6, 'IBRX100'),
            (7, 'Saneamento'),
            (8, 'Eletrica'),
            (9, 'Bancos'),
            (10, 'Seguros'),
            (11, 'Saude'),
            (12, 'Carteira Valor'),

        ], widget=forms.Select
    )



