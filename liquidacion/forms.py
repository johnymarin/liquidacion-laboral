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
    # FIXME make the two field validation works or delete it and go with javascript
    def clean(self):
        cleaned_data = super(LiquidacionForm, self).clean()

        v_fecha_inicio = cleaned_data.get('fecha_inicio')
        v_fecha_finalizacion = cleaned_data.get('fecha_finalizacion')

        if v_fecha_inicio and v_fecha_finalizacion:
            if v_fecha_finalizacion < v_fecha_inicio:
                raise forms.ValidationError("you ha")



class TerminoFijoForm(LiquidacionForm):
    class Meta:
        model = Liquidacion
        exclude =['aplica_art_310', 'salario_diario', 'dias_semanales', 'avance_del_contrato']


class ObraLaborForm(LiquidacionForm):
    class Meta:
        model = Liquidacion
        exclude =['salario_diario', 'dias_semanales']

# TODO write a form for simplified form indefinido
class IndefinidoForm(LiquidacionForm):
    class Meta:
        model = Liquidacion
        exclude =['fecha_finalizacion','aplica_art_310', 'salario_diario', 'dias_semanales', 'avance_del_contrato']

# TODO write a form for simplified form servicio/por dias

