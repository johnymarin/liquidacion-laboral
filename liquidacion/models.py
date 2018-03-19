from datetime import timedelta, date, datetime

from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext

import datos_laborales.models
import datos_tributarios.models

import inspect


# Create your models here.
class Liquidacion(models.Model):



    INDEFINIDO='ind'
    FIJO='fij'
    OBRA='obr'
    TIPOS_DE_CONTRATO = (
        (INDEFINIDO,'Contrato Indefinido'),
        (FIJO, 'Termino Fijo'),
        (OBRA, 'Por Obra o Labor')
    )


    EMP_CONFIANZA= 'confianza'
    EMP_CONSTRUCCION= 'construccion'
    EMP_DOMESTICO= 'domestico'
    EMP_NORMAL= 'normal'
    EMP_INTEGRAL= 'integral'
    TIPOS_DE_SALARIO = (
        (EMP_CONFIANZA, 'Empleado De Confianza (sin h. extras)'),
        (EMP_NORMAL, 'Salario Normal'),
        (EMP_INTEGRAL, 'Salario Integral (superior a 10 minimos)'),
        (EMP_CONSTRUCCION, 'Construccion (por jornal durante una obra)'),
        (EMP_DOMESTICO, 'Empleado Domestico (por jornal varios dias a la semana)')
    )

    SIN_JUSTA_CAUSA ='sin'
    CON_JUSTA_CAUSA ='con'
    RENUNCIA ='ren'
    CAUSAS_DE_TERMINACION = (
        (SIN_JUSTA_CAUSA, 'Despido Sin Justa Causa'),
        (CON_JUSTA_CAUSA, 'Despido Con Justa Causa'),
        (RENUNCIA, 'Renuncia Voluntaria')
    )

    empresa = models.CharField(max_length=200, verbose_name='empresa contratante', blank=True,
                               help_text="""Razon social de la empresa que liquida (este campo es opcional)""")
    empleado=models.CharField(max_length=200, verbose_name='nombre del empleado', blank=True,
                              help_text="""Nombre del empleado a liquidar las prestaciones sociales""")
    clase_contrato = models.CharField(max_length=200, verbose_name='clase de contrato', default=FIJO,
                                      choices=TIPOS_DE_CONTRATO, help_text="""Indica que tipo de contrato se está
                                      liquidando""")
    tipo_salario = models.CharField(max_length=30, default=EMP_NORMAL, choices=TIPOS_DE_SALARIO,
                                    help_text="""Indica si el salario tiene alguna condicion especial, como puede ser
                                    pago por jornales, salario integral o salarios sin derecho a horas extras""")
    fecha_inicio = models.DateField(default=date(now().year-1, now().month, now().day),
                                    help_text="""Fecha en la cual inicio el contrato de trabajo que se pretende liquidar""")
    fecha_liquidacion = models.DateField(default=date(now().year, now().month, now().day),
                                         help_text="""La fecha en la cual se paga la liquidacion del contrato ya sea por despido,
                                         por renuncia o simplemente por vencimiento""")
    fecha_finalizacion = models.DateField(default=None,
                                          help_text="""Solo para contratos a termino fijo o por obra y labor:
                                          Corresponde a la fecha que se acordo iba a finalizar el contrato """)
    causal_terminacion = models.CharField(max_length=200, verbose_name='motivo terminacion del contrato',
                                          choices=CAUSAS_DE_TERMINACION, default=CON_JUSTA_CAUSA,
                                          help_text="""Indica porque terminó el  contrato laboral""")
    cesantias_consignadas = models.BooleanField(verbose_name='Le consignaron las cesantias en el fondo?', default=True,
                                         help_text="""La ley establece que a mas tardar el dia 14 de febrero de cada
                                         año el empleador debe consignar las cesantias de su empleado en el fondo.
                                         por favor indique si esta condición se ha cumplido""")
    demanda_salarios_caidos = models.BooleanField(verbose_name='demandado por salarios caidos?',
                                                  default=False,
                                                  help_text="""Los salarios caidos es una indemnizacion moratoria,
                                                  que se debe pagar cuando al finalizar el contrato no se liquidaron
                                                  las prestaciones sociales.
                                                  En este caso se pregunta si se ha realizado una demanda por este
                                                  concepto antes de dos años de finalizado el contrato""")
    aplica_art_310 = models.BooleanField(verbose_name='Aplica el art. 310 CST?', default=True,
                                         help_text="""El articulo 310 es un regimen especial para las cesantias de los
                                         empleados de la construccion, sin embargo existe una polemica sobre si esta vigente
                                         o derogado tacitamente.
                                         Indica si se calculará considerando este articulo o si se hara con el regimen general""")
    ultimo_salario = models.DecimalField(decimal_places=2,max_digits=14, default=0,
                                         help_text="""Hace referencia al ultimo salario basico que recibio el
                                         trabajador por un (1) mes de trabajo.""")
    salario_diario = models.DecimalField(decimal_places=2, max_digits=14, default=0,
                                         help_text="""En el caso de trabajadores que trabajan por jornal o medio tiempo,
                                         indica el salario basico por un (1) dia de trabajo""")
    dias_semanales = models.DecimalField(decimal_places=0, max_digits=14, default=7,
                                         help_text="""Solo para quienes trabajen por jornal.
                                         Indica el numero de dias a la semana que se trabajaba.""")
    avance_del_contrato = models.DecimalField(decimal_places=2, max_digits=5, default=100,
                                              help_text="""Solo para los contratos de obra o labor, el avance de la obra
                                              o de la labor especifica, en el momento del despido del trabajador""")
    horas_extra_primer_semestre = models.FloatField(max_length=15, default=0,
                                                    help_text="""Indica el dinero total en pesos, pagado por horas extra
                                                     durante el primer semestre.""")
    horas_extra_segundo_semestre = models.FloatField(max_length=15, default=0,
                                                     help_text="""Indica el dinero total en pesos, pagado por horas extra
                                                      durante el segundo semestre.""")
    horas_extra_pendientes = models.FloatField(max_length=15, default=0,
                                               help_text="""Para los salarios pendientes por pagar indica el pago pendiente
                                               por concepto de horas extra.""")
    dias_nomina = models.DecimalField(decimal_places=0, max_digits=14, default=15,
                                      help_text="""El numero de dias de nomina pendientes por pagar a la hora de liquidar""")
    bonificaciones_pendientes = models.FloatField(max_length=15, default=0,
                                                  help_text="""Para los salarios pendientes por pagar indica el pago pendiente por
                                        concepto de bonificaciones""")
    bonificaciones_primer_semestre = models.DecimalField(decimal_places=2,max_digits=14, default=0,
                                                         help_text="""Total pagado por concepto de bonificaciones, comisiones o
                                                         cualquiera que sea la denominacion que se de, durante el primer semestre""")
    bonificaciones_segundo_semestre = models.DecimalField(decimal_places=2,max_digits=14, default=0,
                                                         help_text="""Total pagado por concepto de bonificaciones, comisiones o
                                                         cualquiera que sea la denominacion que se de, durante el segundo semestre.""")
    dias_suspencion_primer_semestre = models.IntegerField(verbose_name='dias de suspencion 1er Semestre', default=0,
                                                          help_text="""El total de dias de suspencion del contrato durante
                                                          el primer semestre. (las incapacidades NO cuentan como suspencion,
                                                          se trata es de aquellos dias que se otorgó permiso o que se sanciono
                                                          al trabajador)""")
    dias_suspencion_segundo_semestre = models.IntegerField(verbose_name='dias de suspencion 2do Semestre', default=0,
                                                           help_text="""El total de dias de suspencion del contrato durante
                                                           el segundo semestre. (las incapacidades NO cuentan como suspencion,
                                                           se trata es de aquellos dias que se otorgó permiso o que se sanciono
                                                           al trabajador)""")
    dias_vacaciones_disfrutados = models.IntegerField(verbose_name='dias de vacaciones disfrutados', default=0,
                                                      help_text="""El numero total de dias de vacaciones que ha disfrutado
                                                      correspondientes al periodo laborado (no cuentan vacaciones de periodos
                                                      anteriores)""")
    porcentaje_descuento_prestamos = models.FloatField(max_length=6, default=0.0, verbose_name='porcentaje descuento libranza',
                                                       help_text="""Porcentaje de descuento que le hacen por concepto de
                                                       libranza""")
    cuota_descuento_libranza = models.DecimalField(decimal_places=2, default=0, max_digits=14,
                                                   help_text="""En caso que le descuenten una suma mensual se puede  indicar
                                                   en este campo.""")
    cuota_embargos_al_salario = models.DecimalField(decimal_places=2, default=0, max_digits=14,
                                                   help_text="""En caso que tenga embargado una suma mensual se puede  indicar
        en este campo.""")

    # TODO calcular cuanto se debio consignar por concpeto de cesantias
    aportes_fondo_empleados = models.DecimalField(decimal_places=2, default=0, max_digits=14,
                                                  help_text="""Valor descontado por aportes al fondo de empleados""")
    aportes_cooperativas = models.DecimalField(decimal_places=2,default=0, max_digits=14,
                                               help_text="""Valor descontado por aportes en coopertivas""")

    def my_get_doc(self, p_name):
        "do nothing"
        my_atribbute = inspect.getattr_static(self, p_name)
        translated = ugettext(my_atribbute)
        return translated



    @property
    def salario_minimo(self):
        """ El salario minimo, que se le paga a cualquier empleado al momento de terminar el contrato de trabajo.

        Para el caso de las personas con contrato a termino indefinido, como su contrato no contempla finalizacion
        se debe considerar el salario minimo vigente en el año al momento de la liquidacion, para  los demas tipos de
        contratos se debe considerar que la fecha de la liquidacion puede ser antes o despues  de la fecha estipulada
        como la finalizacion del contrato.

        :return: El salario minimo en el año de terminacion
        """
        if self.clase_contrato == self.INDEFINIDO or self.fecha_finalizacion is None:
            fecha = self.fecha_liquidacion
        else :
            fecha = min(self.fecha_finalizacion, self.fecha_liquidacion)
        anio = fecha.year
        instancia = datos_laborales.models.SalarioMinimo.objects.get(pk=anio)
        return instancia

    @property
    def foo(self):
        "foooo fooo fooo"
        feo = inspect.getattr_static(self, 'foo')
        pass









    @property
    def salario_basico(self):
        """Salario basico promedio, que gana el empleado en el periodo en que se hace la liquidacion.

        Salario base no puede ser inferior al salario minimo mensual legal vigente,
        para los salarios variables o semi variables se hace el calculo del promedio
        incluyendo las comisiones o bonificaciones y excluyendo horas extras
        y para las personas que trabajan por dias el salario basico es el equivalente al mensual teniendo en cuenta
        semanas en un año de 360 dias (Un dia real equivale a 1,07 dias aproximadamente)

        :return: El salario promedio mensual que gana un empleado o el salario minimo mensual vigente. En caso de
        las personas que devengan un jornal retorna el salario promedio diario o el salario minimo diario.
        """
        es_jornal = self.tipo_salario in (self.EMP_DOMESTICO, self.EMP_CONSTRUCCION)
        if not es_jornal:
            ultimo = float(self.ultimo_salario)
            minimo = float(self.salario_minimo.smmlv)
            variable = (float(self.bonificaciones_primer_semestre)+float(self.bonificaciones_segundo_semestre))/12
            promedio = ultimo + variable
            formula = max(minimo, promedio)
            return round(formula,2)
        else:
            dias_semanales = float(self.dias_semanales)
            dias_factor_semanal = dias_semanales * 30 / 7
            minimo_diario = float(self.salario_minimo.smdlv)
            salario_diario = float(self.salario_diario)
            variable_diario = (float(self.bonificaciones_primer_semestre)+float(self.bonificaciones_segundo_semestre))/360
            promedio_diario = salario_diario + variable_diario
            formula = max(minimo_diario, promedio_diario) * dias_factor_semanal
            return round(formula,2)
    def explicacion_salario_basico(self):
        return self.my_get_doc('salario_basico')



    @property
    def auxilio_transporte(self):
        """Remuneracion entregada al empleador para facilitar su movilizacion hasta el lugar de trabajo.

        Solo tienen derecho al auxilio de transporte aquellos que ganen menos de dos salarios minimos mensuales.
        el auxilio de trasnporte no es un pago que constituya salario, por lo tanto no se incluye en  el calculo de
        aportes parafiscales ni de aportes a seguridad social, pero si se incluye para calcular las prestaciones sociales
        segun el articulo 7 de la ley 01 de 1963.

        :return: El valor del auxilio de transporte mensual o diario en caso de tener derecho, o cero en caso contrario.
        """
        es_jornal = self.tipo_salario in (self.EMP_DOMESTICO, self.EMP_CONSTRUCCION)
        if not es_jornal:
            tiene_auxilio = self.ultimo_salario < (self.salario_minimo.smmlv*2)
            if tiene_auxilio :
                return round(float(self.salario_minimo.aux_trans),2)
            else:
                return 0.00
        else:
            tiene_auxilio_diario = self.salario_diario < (self.salario_minimo.smdlv*2)
            if tiene_auxilio_diario:
                dias_semanales = float(self.dias_semanales)
                dias_factor_semanal = dias_semanales * 30 / 7
                return float(self.salario_minimo.aux_trans_diario) * dias_factor_semanal
            else:
                return 0.00

    @property
    def horas_extra(self):
        """Suma de las horas extra del primer y del segundo semestre.

        Consolida el valor calculado por horas extra cada semestre semestre.

        :return: la suma del valor por horas extra el primer semestre y el valor por horas extra el segundo semestre.
        """
        return self.horas_extra_primer_semestre + self.horas_extra_segundo_semestre

    @property
    def bonificaciones(self):
        """Suma de las bonificaciones del primer y segundo semestre.

        Consolida el valor calculado por bonificaciones del primer y del segundo semestre.

        :return: La suma del valor por bonificacones del primer semestre y el valor por bonificaciones del segundo
        semestre.
        """
        return self.bonificaciones_primer_semestre + self.bonificaciones_segundo_semestre


    @property
    def subtotal_pagos(self):
        """Subtotal por concepto de pagos al empleado.

        :return: la suma de salario basico, auxilio de transporte, horas extra y bonificaciones.
        """
        formula = 0
        for campo in (self.salario_basico, self.auxilio_transporte, self.horas_extra, self.bonificaciones):
            formula += float(campo)
        return formula




# TODO corregir pues la uvt se determina igual que la liquidacion
    @property
    def uvt(self):
        """Unidad de Valor Tributario en la fecha de pago al empleado.

        La unidad de valor tributario (UVT) tiene como fin reemplazar los valores tributarios en  moneda legal, con
        el fin de estandarizar y homogeneizar los distintos valores tributarios.

        :return: La UVT del año en el cual se efectua la liquidacion.
        """
        unidad = datos_tributarios.models.UnidadValorTributario.objects.get(vigencia_UVT=self.fecha_liquidacion.year)
        return unidad

    @property
    def porcentaje_aportes_salud(self):
        """Porcentaje de Aportes en Salud.

        En colombia existe un porcentaje de aportes en salud y pension que deben cotizar tanto los empleadores como,
        los empleados.

        :return: El Aporte del empleado en Salud.
        """
        aport = datos_laborales.models.AporteSalud.objects.filter(inicio_vigencia__lt=self.fecha_liquidacion).order_by('-inicio_vigencia')
        return aport[0]

    @property
    def porcentaje_aporte_pension(self):
        """Porcentaje de Aportes en Pension.

        En colombia existe un porcentaje de aportes en salud y pension que deben cotizar tanto los empleadores como,
        los empleados.

        :return: El Apprte del empleado en Pension.
        """
        aport = datos_laborales.models.AportePension.objects.filter(inicio_vigencia__lt=self.fecha_liquidacion).order_by('-inicio_vigencia')
        return aport[0]

#SECCION PAGOS PRESTACIONALES
    @property
    def dias_suspencion_total(self):
        """
        Los dias de suspencion son utilizados para deducirlos de las prestaciones
        :return: retorna la suma de los dias de suspencion en el primer y segundo semestre
        """
        dias_susp_prim = float(self.dias_suspencion_primer_semestre)
        dias_susp_segu = float(self.dias_suspencion_segundo_semestre)
        formula = dias_susp_prim + dias_susp_segu
        return formula


    @property
    def dias_trabajados_anual(self):
        """" Total dias trabajados en un año.

        El valor de las cesantias que se aportan al fondo de pension en ningun caso puede ser mayor a 360 dias debido
        a que o se pagan al finalizar el contrato o se consignan el 14 de febrero de cada año al fondo.

        :return diferencia entre la fecha de terminacion del contrato y la fecha de inicio, expresada en dias,
        suponiendo 12 meses de 30 dias, no puede ser mayor a 360 dias.
        """
        diasdif = (
            ((self.fecha_liquidacion.year*12 + self.fecha_liquidacion.month)*30 + min(self.fecha_liquidacion.day,30))-
            ((self.fecha_inicio.year*12 + self.fecha_inicio.month)*30 + min(self.fecha_inicio.day,30))
        )

        # TODO validar los casos mayores a 360 dias
        # TODO  agregar un aviso indicando que se superaron los 360 dias y se debe dividir el calculo
        return max(min(diasdif + 1, 360),0)

    @property
    def dias_trabajados_anio_actual(self):
        """
        Es el número de dias que se trabajo durante este año, se utiliza para  conocer cuanto se debe pagar  de cesantias
        y cuanto se debio consignar en el fondo a mas tardar el dia 14 de febrero
        """
        diasdif = (
            ((self.fecha_liquidacion.year*12 + self.fecha_liquidacion.month)*30 + min(self.fecha_liquidacion.day,30))-
            max(
                ((self.fecha_liquidacion.year*12 + 1)*30 + 1),
                ((self.fecha_inicio.year*12 + self.fecha_inicio.month)*30 + min(self.fecha_inicio.day,30))
            )
        )
        diasdif = diasdif + 1
        return max(0, diasdif)

    @property
    def dias_trabajados_primer_semestre(self):
        """diferencia entre la finalizacion del primer semestre y
        el mayor entre la fecha de inico del trabajo o el primero de enero del año en curso
        """
        fecha_inicial = max(self.fecha_inicio, date(self.fecha_liquidacion.year, 1, 1))

        fecha_final = min(self.fecha_liquidacion, date(self.fecha_liquidacion.year, 6, 30))
        if (fecha_inicial > date(self.fecha_liquidacion.year, 6, 30)):
            return 0.00
        else:
            diasdif = (
                ((fecha_final.year*12 + fecha_final.month)*30 + min(fecha_final.day,30))-
                ((fecha_inicial.year*12 + fecha_inicial.month)*30 + min(fecha_inicial.day, 30))
            )
            return max(0, diasdif + 1)

    @property
    def dias_trabajados_segundo_semestre(self):
        """diferencia entre la finalizacion del segundo semestre y
        el mayor entre la fecha de inico del trabajo o el primero de julio del año en curso
        """
        fecha_inicial = max(self.fecha_inicio, date(self.fecha_liquidacion.year, 7, 1))
        fecha_final = min(self.fecha_liquidacion, date(self.fecha_liquidacion.year, 12, 30))

        if (fecha_final < date(self.fecha_liquidacion.year, 7, 1)):
            return 0.00
        else:
            diasdif = (
                ((fecha_final.year*12 + fecha_final.month)*30 + min(fecha_final.day,30))-
                ((fecha_inicial.year*12 + fecha_inicial.month)*30 + min(fecha_inicial.day, 30))
            )
            return max(0, diasdif + 1)


    @property
    def salario_promedio_semestre1(self):
        """retorna el salario promedio mensual durante el primer semestre"""
        salario = float(self.salario_basico)
        horas_extra = float(self.horas_extra_primer_semestre)/6
        formula = salario + horas_extra
        return formula

    @property
    def salario_promedio_semestre2(self):
        """retorna el salario promedio mensual durante el segundo semestre"""
        salario = float(self.salario_basico)
        horas_extra = float(self.horas_extra_segundo_semestre) / 6
        formula = salario + horas_extra
        return formula

    @property
    def salario_promedio(self):
        """retorna el salario promedio mensual durante el año"""
        prom1 = float(self.salario_promedio_semestre1)
        prom2 = float(self.salario_promedio_semestre2)
        formula = (prom1 + prom2)/2
        return formula
    #TODO make cesantias consignadas field, it verifies if  the 14 feb is over and
    # TODO make two new properties total cesantias y consignacion cesantias
    @property
    def pago_total_cesantias (self):
        """
        pago correspondiente a las cesantias, salario basico * dias / 360
        debe incluir el auxilio de transporte pues aunque no sea un pago salarial la norma lo ordena.
        solamente para empleados de la construccion se paga 3 dias por cada mes laborado segun el artuculo 310 del
        codigo laboral, sin embargo existe una discusion puesto que esta norma estaria derogada
        tacitamente por la ley 50/1990
        """
        aplica_art_310 = self.aplica_art_310 and self.tipo_salario==Liquidacion.EMP_CONSTRUCCION
        salario_base_con_auxilio = float(self.salario_basico) + float(self.auxilio_transporte)
        dias_trabajados = float(self.dias_trabajados_anual) - float(self.dias_suspencion_total)
        if aplica_art_310:
            formula = salario_base_con_auxilio * dias_trabajados / 300
            return round(formula, 2)
        else:
            formula = salario_base_con_auxilio * dias_trabajados / 360
            return round(formula, 2)

    @property
    def pago_cesantias_anio_actual(self):
        """
        pago que se debe entregar al trabajador en caso de haber terminado o liquidado el contrato antes de
        haberse consignado en el fondo, se calculan los dias trabajados a partir de enero primero de este año o  si se
        inicio el contrato este año se toma la fecha de inicio, y  se multiplican por el salario y  se divide por el factor
        que depende si aplica art 310 o no.
        """
        aplica_art_310 = self.aplica_art_310 and self.tipo_salario==Liquidacion.EMP_CONSTRUCCION
        salario_base_con_auxilio = float(self.salario_basico) + float(self.auxilio_transporte)
        dias_trabajados = float(self.dias_trabajados_anio_actual) - float(self.dias_suspencion_total)
        if aplica_art_310:
            formula = salario_base_con_auxilio * dias_trabajados / 300
            return round(formula, 2)
        else:
            formula = salario_base_con_auxilio * dias_trabajados / 360
            return round(formula, 2)

    @property
    def cesantias_consignadas_fondo(self):
        """
        valor consignado en el fondo  de pensiones, del total de cesantias ganadas, se restan las que se ganaron durante
        el año de la liquidacion.
        """
        cesantias_totales = float(self.pago_total_cesantias)
        cesantias_actuales = float(self.pago_cesantias_anio_actual)
        formula = max(cesantias_totales - cesantias_actuales, 0)
        return round(formula, 2)


    @property
    def pago_intereses_cesantias (self):
        """pago correspondiente a los intereses de las cesantias: cesantias * 12% * dias / 360 """
        cesantias = float(self.pago_total_cesantias)
        dias_trabajados = float(self.dias_trabajados_anual)
        formula = cesantias * dias_trabajados * 0.12 / 360
        return round(formula, 2)

    @property
    def pago_prima_junio(self):
        """
        para el calculo de la base es necesario sumar el auxilio de transporte (si lo hubiere)
        pago correspondiente a la prima de junio: salario basico mensual  * dias trabajado semestre / 360
        """
        salario_base_con_auxilio = float(self.salario_promedio_semestre1) + float(self.auxilio_transporte)
        dias_trabajados =int(self.dias_trabajados_primer_semestre)
        formula = salario_base_con_auxilio * dias_trabajados/360
        return  round(formula, 2)

    @property
    def pago_prima_diciembre(self):
        """
        para el calculo de la base es necesario sumar el auxilio de transporte (si lo hubiere)
        pago correspondiente a la prima de diciembre: salario basico mensual  * dias trabajado semestre / 360
        """
        salario_promedio = float(self.salario_promedio_semestre2) + float(self.auxilio_transporte)
        dias_trabajados = float(self.dias_trabajados_segundo_semestre)
        formula = salario_promedio * dias_trabajados/360
        return  round(formula, 2)

    @property
    def pago_vacaciones(self):
        """
        para el calculo de la base es necesario restar del salario promedio las h. extra y no se incluye el aux transporte
        pago correspondiente a las vacaciones salario mensual basico * dias trabajados año / 720
        """
        horas_extra_promedio = (float(self.horas_extra_primer_semestre) + float(self.horas_extra_segundo_semestre))/12
        salario_base_sin_extras = float(self.salario_promedio) - horas_extra_promedio
        dias_disfrutados = float(self.dias_vacaciones_disfrutados)
        dias_trabajados = float(self.dias_trabajados_anual) - dias_disfrutados
        formula = salario_base_sin_extras * dias_trabajados / 720
        return round(formula, 2)

    @property
    def subtotal_prestaciones(self):
        "suma subtotal de los pagos correspondientes a prestaciones "
        formula = 0
        for campo in  (self.pago_total_cesantias, self.pago_intereses_cesantias,
                       self.pago_prima_junio, self.pago_prima_diciembre,
                       self.pago_vacaciones):
            formula = formula + float(campo)
        return formula

#SECCION SALARIOS


    @property
    def pago_salarios(self):
        "el salario base multiplicados por los dias en nomina"
        formula = float(self.salario_basico)*float(self.dias_nomina)/30
        return round(formula, 2)


    @property
    def pago_extras(self):
        """retorna la el promedio mensual de horas extras de los ultimos 6 meses"""
        extras = self.horas_extra_pendientes
        return extras

    @property
    def subtotal_pago_nomina(self):
        "suma subtotal de los pagos correspondientes a salarios"
        formula = 0
        for campo in (self.pago_salarios, self.pago_extras, self.bonificaciones_pendientes):
            formula += float(campo)
        return formula

#SECCION INDEMNIZACION
    @property
    def pago_indemnizacion(self):
        "si el despido fue sin causa justa se debe pagar la indemnizacion correspondiente"
        if self.causal_terminacion == self.SIN_JUSTA_CAUSA:
            salario_base_diario = float(self.salario_basico) / 30
            if self.clase_contrato == self.FIJO:
                fecha_final = self.fecha_finalizacion
                fecha_inicial = self.fecha_liquidacion
                if fecha_final is None:
                    fecha_final = fecha_inicial

                dias_faltantes = (
                    ((fecha_final.year * 12 + fecha_final.month) * 30 + min(fecha_final.day, 30)) -
                    ((fecha_inicial.year * 12 + fecha_inicial.month) * 30 + min(fecha_inicial.day, 30))
                    +1
                )

                dias = max(dias_faltantes, 15)

                indem_fijo = dias * salario_base_diario
                return indem_fijo
            elif self.clase_contrato == self.INDEFINIDO:
                fecha_final = self.fecha_liquidacion
                fecha_inicial = self.fecha_inicio
                diasdif = (
                    ((fecha_final.year * 12 + fecha_final.month) * 30 + min(fecha_final.day, 30)) -
                    ((fecha_inicial.year * 12 + fecha_inicial.month) * 30 + min(fecha_inicial.day, 30))
                    +1
                )
                dias = 30 + max(diasdif - 360, 0) * 20 / 360
                indem_indefinido = dias * salario_base_diario
                return indem_indefinido
            elif self.clase_contrato == self.OBRA:
                avance = float(self.avance_del_contrato)
                fecha_inicial = self.fecha_inicio
                fecha_final = self.fecha_liquidacion
                dias_avance = (
                    ((fecha_final.year * 12 + fecha_final.month) * 30 + min(fecha_final.day, 30)) -
                    ((fecha_inicial.year * 12 + fecha_inicial.month) * 30 + min(fecha_inicial.day, 30))
                    +1
                )
                dias_faltantes = dias_avance * (100/avance -1)
                dias = max(dias_faltantes, 15)
                indem_obra = dias * salario_base_diario
                return indem_obra
        else:
            return 0.00

    @property
    def pago_indemnizacion_interes(self):
        "esta procede solo en el caso que el fondo de pension demora injustificadamente el pago "\
        "y solo si proviene del sistema general de pensiones"
        return 0.00

    @property
    def pago_indemnizacion_moratoria(self):
        """
        solo procede cuando un juez comprueba que hubo mala fe en el no pago de las prestaciones sociales
        """
        fecha_final = self.fecha_liquidacion
        fecha_inicial = self.fecha_finalizacion
        if self.fecha_finalizacion is None:
            return 0.00
        elif fecha_inicial >= fecha_final:
            return 0.00
        elif fecha_inicial < fecha_final:
            dias = (
                ((fecha_final.year * 12 + fecha_final.month) * 30 + min(fecha_final.day, 30)) -
                ((fecha_inicial.year * 12 + fecha_inicial.month) * 30 + min(fecha_inicial.day, 30))
                + 1
            )
            if (self.demanda_salarios_caidos):
                formula = (min(dias, 720) * self.ultimo_salario / 30)
                formula = (formula + self.pago_salarios) * (0.16 / 100) * max(dias - 720, 0)
            else:
                formula = (self.pago_salarios) * (0.16 / 100) * dias
            return formula

    @property
    def pago_indemnizacion_cesantias(self):
        if self.fecha_finalizacion is None:
            return 0.00
        elif self.cesantias_consignadas:
            return 0.00
        else:
            fecha_consignacion = min(self.fecha_finalizacion, self.fecha_liquidacion)
            fecha_consignacion = date(fecha_consignacion.year,2,14)
            dias = max((self.fecha_liquidacion - fecha_consignacion).days,0)
            formula = (self.ultimo_salario/30)*dias
            return round(formula,2)

    @property
    def subtotal_indemnizaciones(self):
        "subtotal con las sumas a pagar por indemnizaciones si un juez asi lo decide"
        formula = 0.00
        for campo in (self.pago_indemnizacion, self.pago_indemnizacion_moratoria, self.pago_indemnizacion_cesantias):
            formula = formula + float(campo)
        return formula

#SECCION DEDUCCIONES
    @property
    def deduccion_pension(self):
        formula = self.subtotal_pago_nomina * self.porcentaje_aporte_pension.porcentaje_aporte_empleado
        return round(formula, 2)

    @property
    def deduccion_salud(self):
        formula = self.subtotal_pago_nomina * self.porcentaje_aportes_salud.porcentaje_aporte_empleado
        return round(formula,2)

    @property
    def deduccion_retefuente_indemnizacion(self):
        "retorna el valor correspondiente a la retencion en la fuente por las indemnizaciones."
        limite = 204 * self.uvt.valor_UVT
        if self.salario_promedio <= limite:
            return 0.00
        elif self.salario_promedio > limite:
            execnto = self.subtotal_indemnizaciones * 0.25
            formula = (self.subtotal_indemnizaciones - execnto)*0.20
            return round(formula, 2)

    @property
    def maximo_deducible(self):
        "maximo que se le puede deducir a una persona sin afectar el 50% de un salario minimo"
        formula = (self.subtotal_pago_nomina - self.deduccion_salud - self.deduccion_pension) - float(self.salario_minimo.smmlv) / 2.0
        return formula

    @property
    def deduccion_prestamos(self):
        "en prestamos ordinarios solo se puede deducir maximo una quinta parte de lo que exceda al salario minimo"
        maximo_deducible_en_prestamos= 0
        for campo in (self.subtotal_pago_nomina, -1* self.deduccion_salud, -1* self.deduccion_pension, -1* self.salario_minimo.smmlv):
            maximo_deducible_en_prestamos = maximo_deducible_en_prestamos + float(campo)
        maximo_deducible_en_prestamos = (maximo_deducible_en_prestamos) / 5.0
        formula = float(self.subtotal_pago_nomina) * float(self.porcentaje_descuento_prestamos)
        formula = min(formula, maximo_deducible_en_prestamos, float(self.maximo_deducible))
        return round(formula, 2)

    @property
    def deduccion_fondo_empleados(self):
        "los aprtes a fondo de empleados no pueden ser mayores al 10% del salario o disminuir el salario por menos de un salario minimo"
        formula = min(self.aportes_fondo_empleados, self.maximo_deducible, self.subtotal_pago_nomina * 0.10)
        return round(formula, 2)

    @property
    def deduccion_cooperativas(self):
        "las deducciones de cooperativas no puede superar el 50% del salario ni afectar el minimo vital"
        formula = min(self.aportes_cooperativas, self.maximo_deducible)
        return round(formula, 2)



    @property
    def deduccion_libranzas(self):
        """"las deducciones por libranzas no pueden superar el minimo vital, antes de verificar el minimo
        se totalizan  los campos de porcentaje deduccion libranzas y cuota deduccion libranzas"""
        porcentaje = float(self.porcentaje_descuento_prestamos)
        salario = float(self.salario_basico)
        cuota = float(self.cuota_descuento_libranza)
        descuento_libranzas = porcentaje*salario + cuota
        maximo_deducible = float(self.maximo_deducible)
        formula = min(descuento_libranzas, maximo_deducible)
        return round(formula, 2)

    @property
    def subtotal_deducciones(self):
        formula = 0
        for campo in (self.deduccion_pension, self.deduccion_salud, self.deduccion_retefuente_indemnizacion,
                      self.deduccion_prestamos, self.deduccion_fondo_empleados,
                      self.deduccion_cooperativas, self.deduccion_libranzas):
            formula = formula + float(campo)
        formula = min(formula, self.maximo_deducible)
        return formula

    @property
    def total_liquidacion_a_favor_empleado(self):
        formula = 0
        for campo in(self.subtotal_pago_nomina, self.subtotal_prestaciones, self.subtotal_indemnizaciones,
                      -self.subtotal_deducciones):
            formula =  formula + float(campo)
        return round(formula, 2)


