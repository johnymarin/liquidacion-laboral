# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-24 21:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Liquidacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empresa', models.CharField(blank=True, help_text='El nombre de la empresa', max_length=200, verbose_name='empresa contratante')),
                ('empleado', models.CharField(blank=True, max_length=200, verbose_name='nombre del empleado')),
                ('fecha_inicio', models.DateField(default=datetime.datetime(2016, 1, 30, 21, 44, 52, 972374, tzinfo=utc))),
                ('fecha_liquidacion', models.DateField(default=django.utils.timezone.now)),
                ('fecha_finalizacion', models.DateField(default=django.utils.timezone.now)),
                ('causal_terminacion', models.CharField(choices=[('sin', 'Despido Sin Justa Causa'), ('con', 'Despido Con Justa Causa'), ('ren', 'Renuncia Voluntaria')], default='con', max_length=200, verbose_name='motivo terminacion del contrato')),
                ('servicio_domestico', models.BooleanField(default=False, verbose_name='es de servicio domestico')),
                ('clase_contrato', models.CharField(choices=[('ind', 'Contrato Indefinido'), ('fij', 'Termino Fijo'), ('obr', 'Por Obra o Labor')], default='fij', max_length=200, verbose_name='clase de contrato')),
                ('demanda_salarios_caidos', models.BooleanField(default=False, verbose_name='ha entablado demanda salarios caidos antes de 2 años del despido?')),
                ('ultimo_salario', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('salario_diario', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('dias_semanales', models.DecimalField(decimal_places=0, default=15, max_digits=14)),
                ('tipo_salario', models.CharField(choices=[('con', 'Empleado De Confianza (sin h. extras)'), ('nor', 'Contrato Normal'), ('int', 'Salario Integra (superior a 10 minimos)')], default='nor', max_length=30)),
                ('horas_extra_primer_semestre', models.FloatField(default=0, max_length=15)),
                ('horas_extra_segundo_semestre', models.FloatField(default=0, max_length=15)),
                ('horas_extra_pendientes', models.FloatField(default=0, max_length=15)),
                ('dias_nomina', models.DecimalField(decimal_places=0, default=15, max_digits=14)),
                ('bonificaciones_primer_semestre', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('bonificaciones_segundo_semestre', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('dias_suspencion_primer_semestre', models.IntegerField(default=0, verbose_name='dias de suspencion')),
                ('dias_suspencion_segundo_semestre', models.IntegerField(default=0, verbose_name='dias de suspencion')),
                ('dias_vacaciones_disfrutados', models.IntegerField(default=0, verbose_name='dias de vacacion')),
                ('porcentaje_descuento_prestamos', models.FloatField(default=0.0, max_length=6, verbose_name='porcentaje descuento libranza')),
                ('cuota_descuento_libranza', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('aportes_fondo_empleados', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('aportes_cooperativas', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('cuota_libranzas', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
            ],
        ),
    ]
