from django.db import models

# Create your models here.
from django.utils.datetime_safe import date


class UnidadValorTributario(models.Model):
    vigencia_UVT = models.IntegerField(primary_key=True,verbose_name='año de vigencia',default=date.today().year+1)
    valor_UVT = models.DecimalField(decimal_places=2, max_digits=14, default=0, verbose_name='Unidad de valor tributario vigente')

    def __str__(self):
        return 'UVT {self.vigencia_UVT} (${self.valor_UVT:,} COP)'.format(self=self)
