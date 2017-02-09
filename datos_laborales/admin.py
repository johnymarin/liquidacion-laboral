from django.contrib import admin
from .models import SalarioMinimo, AportePension, AporteSalud
# Register your models here.
admin.site.register(SalarioMinimo)
admin.site.register(AportePension)
admin.site.register(AporteSalud)