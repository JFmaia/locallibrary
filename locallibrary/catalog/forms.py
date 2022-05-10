from django import forms
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Digite uma data entre agora e 4 semanas (padrão 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Verifica se um encontro não é no passado.
        if data < datetime.date.today():
            raise ValidationError(_('Data inválida - renovação no passado'))

        # Verifique se uma data está na faixa permitida (+4 semanas a partir de hoje).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Data inválida - renovação com mais de 4 semanas pela frente'))

        # Lembre-se de sempre devolver os dados limpos.
        return data