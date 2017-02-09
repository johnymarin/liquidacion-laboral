from datetime import date

from django.db import models

from django.utils.timezone import now



# Create your models here.
class SalarioMinimo(models.Model):
    vigencia_smmlv = models.IntegerField(primary_key=True,verbose_name='año de vigencia',default=date.today().year+1)
    smmlv = models.DecimalField(decimal_places=2, max_digits=14, default=0, verbose_name='salario minimo vigente')
    aux_trans = models.DecimalField(decimal_places=2, max_digits=14, default=0, verbose_name='auxilio de transporte')
    def _get_smdlv(self):
        "Retorna el salario minimo diario legal vigente."
        formula = float(self.smmlv)/30
        return formula
    smdlv = property(_get_smdlv)

    def _get_variacion_anual(self):
        "Retorna el porcentaje de aumento entre un salario minimo y el anterior"
        try:
            smmlv_vigencia_ant = SalarioMinimo.objects.get(pk=self.pk-1)
            variacion = (self.smmlv - smmlv_vigencia_ant.smmlv) / smmlv_vigencia_ant.smmlv
        except:
            return 0
        else:
            return variacion
    variacion_anual =property(_get_variacion_anual)

    @property
    def aux_trans_diario(self):
        auxilio = float(self.aux_trans)
        formula = auxilio / 30
        return formula

    def __str__(self):
        return 'SMMLV {self.vigencia_smmlv} ({self.smmlv:,} COP)'.format(self=self)

class AporteSalud(models.Model):
    inicio_vigencia = models.DateField(default=now)
    final_vigencia = models.DateField(null=True)
    porcentaje_aporte_empresa = models.FloatField(max_length=6, default=0.0, verbose_name="porcentaje aportado por empresa")
    porcentaje_aporte_empleado = models.FloatField(max_length=6, default=0.0, verbose_name="porcentaje aportado por empleado")


    @property
    def total_porcentaje_aportes(self):
        return self.porcentaje_aporte_empleado + self.porcentaje_aporte_empresa

    def __str__(self):
        return '{self.total_porcentaje_aportes:.2%}' \
               ' ({self.porcentaje_aporte_empresa:.2%} - {self.porcentaje_aporte_empleado:.2%})'.format(self=self)

class AportePension(models.Model):
    inicio_vigencia = models.DateField(default=now)
    final_vigencia = models.DateField(null=True)
    porcentaje_aporte_empresa = models.FloatField(max_length=6, default=0.0, verbose_name="porcentaje aportado por empresa")
    porcentaje_aporte_empleado = models.FloatField(max_length=6, default=0.0, verbose_name="porcentaje aportado por empleado")


    @property
    def total_porcentaje_aportes(self):
        return self.porcentaje_aporte_empleado + self.porcentaje_aporte_empresa

    def __str__(self):
        return '{self.total_porcentaje_aportes:.2%}' \
               ' ({self.porcentaje_aporte_empresa:.2%} - {self.porcentaje_aporte_empleado:.2%})'.format(self=self)