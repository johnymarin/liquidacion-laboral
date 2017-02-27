from datetime import timedelta, date


from django.db import models
from django.utils.timezone import now
import datos_laborales.models
import datos_tributarios.models


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
    fecha_finalizacion = models.DateField(default=date(now().year, now().month, now().day),
                                          help_text="""Solo para contratos a termino fijo o por obra y labor:
                                          Corresponde a la fecha que se acordo iba a finalizar el contrato """)
    causal_terminacion = models.CharField(max_length=200, verbose_name='motivo terminacion del contrato',
                                          choices=CAUSAS_DE_TERMINACION, default=CON_JUSTA_CAUSA,
                                          help_text="""Indica porque terminó el  contrato laboral""")

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
    bonificaciones_primer_semestre = models.DecimalField(decimal_places=2,max_digits=14, default=0,
                                                         help_text="""Total pagado por concept de bonificaciones, comisiones o
                                                         cualquiera que sea la denominacion que se de, durante el primer semestre""")
    bonificaciones_segundo_semestre = models.DecimalField(decimal_places=2,max_digits=14, default=0,
                                                         help_text="""Total pagado por concept de bonificaciones, comisiones o
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
    dias_vacaciones_disfrutados = models.IntegerField(verbose_name='dias de vacacion', default=0,
                                                      help_text="""El numero total de dias de vacaciones que ha disfrutado
                                                      correspondientes al periodo laborado (no cuentan vacaciones de periodos
                                                      anteriores)""")
    porcentaje_descuento_prestamos = models.FloatField(max_length=6, default=0.0, verbose_name='porcentaje descuento libranza',
                                                       help_text="""Porcentaje de descuento que le hacen por concepto de
                                                       libranza""")
    cuota_descuento_libranza = models.DecimalField(decimal_places=2, default=0, max_digits=14,
                                                   help_text="""En caso que le descuenten una suma mensual se puede  indicar
                                                   en este campo.""")
    aportes_fondo_empleados = models.DecimalField(decimal_places=2, default=0, max_digits=14,
                                                  help_text="""Valor descontado por aportes al fondo de empleados""")
    aportes_cooperativas = models.DecimalField(decimal_places=2,default=0, max_digits=14,
                                               help_text="""Valor descontado por aportes en coopertivas""")


    @property
    def salario_minimo(self):

        if self.clase_contrato == self.INDEFINIDO:
            anio = self.fecha_finalizacion.year
        else :
            anio = self.fecha_liquidacion.year

        instancia = datos_laborales.models.SalarioMinimo.objects.get(pk=anio)
        return instancia

    @property
    def salario_basico(self):
        """
        salario base no puede ser inferior al salario minimo mensual legal vigente,
        para los salarios variables o semi variables se hace el calculo del promedio
        incluyendo las comisiones o bonificaciones y excluyendo horas extras
        y para las personas que trabajan por dias el salario basico es el equivalente al mensual teniendo en cuenta
        semanas en un año de 360 dias (Un dia real equivale a 1,07 dias aproximadamente)
        """
        es_jornal = self.tipo_salario in (self.EMP_DOMESTICO, self.EMP_CONSTRUCCION)
        if not es_jornal:
            ultimo = float(self.ultimo_salario)
            minimo = float(self.salario_minimo.smmlv)
            variable = (float(self.bonificaciones_primer_semestre)+float(self.bonificaciones_segundo_semestre))/12
            promedio = ultimo + variable
            formula = max(minimo, promedio)
            return formula
        else:
            dias_semanales = float(self.dias_semanales)
            dias_factor_semanal = dias_semanales * 30 / 7
            minimo_diario = float(self.salario_minimo.smdlv)
            salario_diario = float(self.salario_diario)
            variable_diario = (float(self.bonificaciones_primer_semestre)+float(self.bonificaciones_segundo_semestre))/360
            promedio_diario = salario_diario + variable_diario
            formula = max(minimo_diario, promedio_diario) * dias_factor_semanal
            return formula

    @property
    def pago_auxilio_transporte(self):
        """
        Solo tienen derecho al auxilio de transporte aquello que ganen menos de dos salarios minimos mensuales.
        el auxilio de trasnporte no es un pago que constituya salario por lo tanto no se incluye en  el calculo de
        aportes parafiscales ni de aportes a seguridad social, pero si se incluye para calcular las prestaciones sociales
        segun el articulo 7 de la ley 01 de 1963
        """
        es_jornal = self.tipo_salario in (self.EMP_DOMESTICO, self.EMP_CONSTRUCCION)
        if not es_jornal:
            tiene_auxilio = self.ultimo_salario < (self.salario_minimo.smmlv*2)
            if tiene_auxilio :
                return float(self.salario_minimo.aux_trans)
            else:
                return 0
        else:
            tiene_auxilio_diario = self.salario_diario < (self.salario_minimo.smdlv*2)
            if tiene_auxilio_diario:
                dias_semanales = float(self.dias_semanales)
                dias_factor_semanal = dias_semanales * 30 / 7
                return float(self.salario_minimo.aux_trans_diario) * dias_factor_semanal
            else:
                return 0



#corregir pues la uvt se determina igual que la liquidacion
    @property
    def uvt(self):
        unidad = datos_tributarios.models.UnidadValorTributario.objects.get(vigencia_UVT=self.fecha_liquidacion.year)
        return unidad

    @property
    def porcentaje_aportes_salud(self):
        aport = datos_laborales.models.AporteSalud.objects.filter(inicio_vigencia__lt=self.fecha_liquidacion,
                                                                final_vigencia__gt=self.fecha_liquidacion)
        return aport[0]

    @property
    def porcentaje_aporte_pension(self):
        aport = datos_laborales.models.AportePension.objects.filter(inicio_vigencia__lt=self.fecha_liquidacion,
                                                                   final_vigencia__gt=self.fecha_liquidacion)
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
        """"
        diferencia entre la fecha de terminacion del contrato y la fecha de inicio, expresada en dias,
         suponiendo 12 meses de 30 dias, por el momento no podra ser mayor a 360 dias
         """
        diasdif = (
            ((self.fecha_liquidacion.year*12 + self.fecha_liquidacion.month)*30 + min(self.fecha_liquidacion.day,30))-
            ((self.fecha_inicio.year*12 + self.fecha_inicio.month)*30 + min(self.fecha_inicio.day,30))
        )
        #pediente validar los casos mayores a 360 dias
        return  min(diasdif + 1, 360)

    @property
    def dias_trabajados_primer_semestre(self):
        """diferencia entre la finalizacion del primer semestre y
        el mayor entre la fecha de inico del trabajo o el primero de enero del año en curso
        """

        fecha_inicial = max(self.fecha_inicio, date(self.fecha_liquidacion.year, 1, 1))

        fecha_final = min(self.fecha_liquidacion, date(self.fecha_liquidacion.year, 6, 30))
        if (fecha_inicial > date(self.fecha_liquidacion.year, 6, 30)):
            return 0
        else:
            diasdif = (
                ((fecha_final.year*12 + fecha_final.month)*30 + min(fecha_final.day,30))-
                ((fecha_inicial.year*12 + fecha_inicial.month)*30 + min(fecha_inicial.day, 30))
            )
            return diasdif + 1

    @property
    def dias_trabajados_segundo_semestre(self):
        """diferencia entre la finalizacion del segundo semestre y
        el mayor entre la fecha de inico del trabajo o el primero de julio del año en curso
        """

        fecha_inicial = max(self.fecha_inicio, date(self.fecha_liquidacion.year, 7, 1))
        fecha_final = min(self.fecha_liquidacion, date(self.fecha_liquidacion.year, 12, 30))

        if (fecha_final < date(self.fecha_liquidacion.year, 7, 1)):
            return 0
        else:
            diasdif = (
                ((fecha_final.year*12 + fecha_final.month)*30 + min(fecha_final.day,30))-
                ((fecha_inicial.year*12 + fecha_inicial.month)*30 + min(fecha_inicial.day, 30))
            )
            return diasdif + 1


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
    @property
    def pago_cesantias (self):
        """
        pago correspondiente a las cesantias, salario basico * dias / 360
        debe incluir el auxilio de transporte pues aunque no sea un pago salarial la norma lo ordena.
        solamente para empleados de la construccion se paga 3 dias por cada mes laborado segun el artuculo 310 del
        codigo laboral, sin embargo existe una discusion puesto que esta norma estaria derogada
        tacitamente por la ley 50/1990
        """
        aplica_art_310 = self.aplica_art_310 and self.tipo_salario==Liquidacion.EMP_CONSTRUCCION
        salario_base_con_auxilio = float(self.salario_basico) + float(self.pago_auxilio_transporte)
        dias_trabajados = float(self.dias_trabajados_anual) - float(self.dias_suspencion_total)
        if aplica_art_310:
            formula = salario_base_con_auxilio * dias_trabajados / 300
            return round(formula, 2)
        else:
            formula = salario_base_con_auxilio * dias_trabajados / 360
            return round(formula, 2)

    @property
    def pago_intereses_cesantias (self):
        """pago correspondiente a los intereses de las cesantias: cesantias * 12% * dias / 360 """
        cesantias = float(self.pago_cesantias)
        dias_trabajados = float(self.dias_trabajados_anual)
        formula = cesantias * dias_trabajados * 0.12 / 360
        return round(formula, 2)

    @property
    def pago_prima_junio(self):
        """
        para el calculo de la base es necesario sumar el auxilio de transporte (si lo hubiere)
        pago correspondiente a la prima de junio: salario basico mensual  * dias trabajado semestre / 360
        """
        salario_base_con_auxilio = float(self.salario_promedio_semestre1) + float(self.pago_auxilio_transporte)
        dias_trabajados =int(self.dias_trabajados_primer_semestre)
        formula = salario_base_con_auxilio * dias_trabajados/360
        return  round(formula, 2)

    @property
    def pago_prima_diciembre(self):
        """
        para el calculo de la base es necesario sumar el auxilio de transporte (si lo hubiere)
        pago correspondiente a la prima de diciembre: salario basico mensual  * dias trabajado semestre / 360
        """
        salario_promedio = float(self.salario_promedio_semestre2) + float(self.pago_auxilio_transporte)
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
        for campo in  (self.pago_cesantias, self.pago_intereses_cesantias,
                       self.pago_prima_junio, self.pago_prima_diciembre,
                       self.pago_vacaciones):
            formula = formula + float(campo)

        return formula

#SECCION SALARIOS


    @property
    def pago_salarios(self):
        "el salario base multiplicados por los dias en nomina"
        formula = self.salario_basico*self.dias_nomina/30
        return formula


    @property
    def pago_extras(self):
        """retorna la el promedio mensual de horas extras de los ultimos 6 meses"""
        extras = self.horas_extra_pendientes
        return extras

    @property
    def subtotal_salarios(self):
        "suma subtotal de los pagos correspondientes a salarios"
        formula = 0
        for campo in (self.pago_salarios, self.pago_extras, self.bonificaciones):
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
            return 0

    @property
    def pago_indemnizacion_interes(self):
        "esta procede solo en el caso que el fondo de pension demora injustificadamente el pago "\
        "y solo si proviene del sistema general de pensiones"
        return 0

    @property
    def pago_indemnizacion_moratoria(self):
        """
        solo procede cuando un juez comprueba que hubo mala fe en el no pago de las prestaciones sociales
        """
        if self.fecha_finalizacion < self.fecha_liquidacion:
            return 0
        elif self.fecha_finalizacion >= self.fecha_liquidacion:
            fecha_final = self.fecha_liquidacion
            fecha_inicial = self.fecha_finalizacion
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
            return 0
        else:
            fecha_consignacion = min(self.fecha_finalizacion, self.fecha_liquidacion)
            fecha_consignacion = date(fecha_consignacion.year,2,14)
            dias = max((self.fecha_liquidacion - fecha_consignacion).days,0)
            formula = (self.ultimo_salario/30)*dias
            return formula

    @property
    def subtotal_indemnizaciones(self):
        "subtotal con las sumas a pagar por indemnizaciones si un juez asi lo decide"
        formula = 0
        for campo in (self.pago_indemnizacion, self.pago_indemnizacion_moratoria, self.pago_indemnizacion_cesantias):
            formula = formula + float(campo)
        return formula

#SECCION DEDUCCIONES
    @property
    def deduccion_pension(self):
        formula = self.subtotal_salarios * self.porcentaje_aporte_pension.porcentaje_aporte_empleado
        return formula
    @property
    def deduccion_salud(self):
        formula = self.subtotal_salarios*self.porcentaje_aportes_salud.porcentaje_aporte_empleado
        return formula

    @property
    def deduccion_retefuente_indemnizacion(self):
        "retorna el valor correspondiente a la retencion en la fuente por las indemnizaciones."
        limite = 204 * self.uvt.valor_UVT
        if self.salario_promedio <= limite:
            return 0
        elif self.salario_promedio > limite:
            execnto = self.subtotal_indemnizaciones * 0.25
            formula = (self.subtotal_indemnizaciones - execnto)*0.20
            return formula

    @property
    def maximo_deducible(self):
        "maximo que se le puede deducir a una persona sin afectar el 50% de un salario minimo"
        formula = (self.subtotal_salarios - self.deduccion_salud - self.deduccion_pension) - self.salario_minimo.smmlv/2
        return formula

    @property
    def deduccion_prestamos(self):
        "en prestamos ordinarios solo se puede deducir maximo una quinta parte de lo que exceda al salario minim"
        maximo_deducible_en_prestamos = (self.subtotal_salarios-self.deduccion_salud- self.deduccion_pension - self.salario_minimo.smmlv)/5
        formula = self.subtotal_salarios*self.porcentaje_descuento_prestamos
        formula = min(formula,maximo_deducible_en_prestamos, self.maximo_deducible)
        return  formula

    @property
    def deduccion_fondo_empleados(self):
        "los aprtes a fondo de empleados no pueden ser mayores al 10% del salario o disminuir el salario por menos de un salario minimo"
        formula = min(self.aportes_fondo_empleados, self.maximo_deducible, self.subtotal_salarios*0.10)
        return formula

    @property
    def dedeccion_cooperativas(self):
        "las deducciones de cooperativas no puede superar el 50% del salario ni afectar el minimo vital"
        formula = min(self.aportes_cooperativas, self.maximo_deducible)
        return formula



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
        return formula

    @property
    def subtotal_deducciones(self):
        formula = sum(self.deduccion_pension, self.deduccion_salud, self.deduccion_retefuente_indemnizacion,
                      self.deduccion_prestamos, self.deduccion_fondo_empleados,
                      self.dedeccion_cooperativas, self.deduccion_libranzas)
        formula = min(formula, self.maximo_deducible)
        return formula

    @property
    def total_liquidacion_a_favor_empleado(self):
        formula = sum(self.subtotal_salarios, self.subtotal_prestaciones, self.subtotal_indemnizaciones,
                      -self.subtotal_deducciones)
        return formula


