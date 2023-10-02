from django import forms
from django.utils import timezone


class HorasForm(forms.ModelForm):
    def clean_date(self):
        date = self.cleaned_data['date']
        if date > timezone.now().date():
            raise forms.ValidationError('La fecha no puede ser en el futuro')
        # La fecha no puede ser de mas de 72 hs en el pasado
        if date < timezone.now().date() - timezone.timedelta(days=3):
            raise forms.ValidationError('La fecha no puede ser de mas de 72 hs en el pasado')
        return date
