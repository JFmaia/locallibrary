from django import forms

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Digite uma data entre agora e 4 semanas (padrão 3).")