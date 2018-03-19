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


class IndefinidoForm(LiquidacionForm):
    class Meta:
        model = Liquidacion
        exclude =['fecha_finalizacion','aplica_art_310', 'salario_diario', 'dias_semanales', 'avance_del_contrato']


class DiasForm(LiquidacionForm):
    class Meta:
        model = Liquidacion
        exclude =['fecha_finalizacion','aplica_art_310' , 'avance_del_contrato', 'ultimo_salario']


class ConfianzaForm(LiquidacionForm):
    class Meta:
        model = Liquidacion
        exclude =['fecha_finalizacion','aplica_art_310', 'salario_diario', 'dias_semanales', 'avance_del_contrato',
                  'horas_extra_primer_semestre', 'horas_extra_segundo_semestre', 'horas_extra_pendientes']


class BasicaForm(LiquidacionForm):
    class Meta:
        model = Liquidacion
        fields = ['fecha_inicio','fecha_liquidacion','ultimo_salario']

class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.CharField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea
    )