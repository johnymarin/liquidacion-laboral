from django import forms
from django.core.exceptions import ValidationError

from .models import Liquidacion

#override date formatting because i think bowser support is nice
forms.DateInput.input_type="date"

class LiquidacionForm(forms.ModelForm):
    class Meta:
        model = Liquidacion
        fields = '__all__'
        localize =False
        widgets = {
            'fecha_finalizacion': forms.DateInput(attrs={'readonly':False, 'class':'myclass'})
        }




    def clean(self):
        cleaned_data = super(LiquidacionForm, self).clean()

        v_fecha_inicio = cleaned_data.get('fecha_inicio')
        v_fecha_finalizacion = cleaned_data.get('fecha_finalizacion')

        if v_fecha_inicio and v_fecha_finalizacion:
            if v_fecha_finalizacion < v_fecha_inicio:
                raise forms.ValidationError("you ha")




