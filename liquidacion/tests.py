from datetime import timedelta, date
from django.test import TestCase
from django.utils.timezone import now

from .models import Liquidacion
from datos_laborales.models import SalarioMinimo

# Create your tests here.
BASE_CESANTIAS_PRIMA = 1100000


def create_salario_minimo(vigencia_smmlv=now().year, smmlv=1000000, aux_trans=100000):
    salario_pasado= SalarioMinimo(pk=now().year-1,vigencia_smmlv=vigencia_smmlv*0.90, smmlv=smmlv*0.90, aux_trans=aux_trans*0.90)
    salario_pasado.save()
    salario_futuro= SalarioMinimo(pk=now().year+1, vigencia_smmlv=vigencia_smmlv*1.10, smmlv=smmlv*1.10, aux_trans=aux_trans*1.10)
    salario_futuro.save()
    salario_actual= SalarioMinimo(pk=now().year, vigencia_smmlv=vigencia_smmlv, smmlv=smmlv, aux_trans=aux_trans)
    salario_actual.save()

def create_liquidacion(p_empresa="EJEMPLO SAS", p_empleado="Johny Marin Gutierrez", p_fecha_inicio=now(),
                       p_fecha_liquidacion=now(), p_demanda_salarios_caidos=False, p_ultimo_salario=1000,
                       p_salario_promedio=1000, p_promedio_horas_extra=1000, p_dias_nominabonificaciones=0,
                       p_otros_ingresos_salariales=1000, p_causal_terminacion="vencimiento", p_dias_suspencion=0,
                       p_clase_contrato="indefinido", p_fecha_finalizacion=now(),
                       p_tipo_salario="normal", p_porcentaje_descuento_prestamos=0.0, p_cuota_descuento_libranza=0,
                       p_aportes_fondo_empleados=0, p_aportes_cooperativas=0, p_cuota_libranzas=0):

    """
    Creates a liquidation with the given parameters
    :param p_fecha_inicial:
    :param p_fecha_final:
    :return: Liquidacion
    """
    i_liquidacion = Liquidacion.objects.create(empresa=p_empresa,empleado=p_empleado,fecha_inicio=p_fecha_inicio,
                                               fecha_liquidacion=p_fecha_liquidacion,
                                               demanda_salarios_caidos=p_demanda_salarios_caidos,
                                               ultimo_salario=p_ultimo_salario,salario_promedio=p_salario_promedio,
                                               promedio_horas_extra=p_promedio_horas_extra,
                                               dias_nominabonificaciones=p_dias_nominabonificaciones,
                                               otros_ingresos_salariales=p_otros_ingresos_salariales,
                                               causal_terminacion=p_causal_terminacion, dias_suspencion=p_dias_suspencion,
                                               clase_contrato=p_clase_contrato,
                                               fecha_finalizacion=p_fecha_finalizacion, tipo_salario=p_tipo_salario,
                                               porcentaje_descuento_prestamos=p_porcentaje_descuento_prestamos,
                                               cuota_descuento_libranza=p_cuota_descuento_libranza,
                                               aportes_fondo_empleados=p_aportes_fondo_empleados,
                                               aportes_cooperativas=p_aportes_cooperativas,
                                               cuota_libranzas=p_cuota_libranzas)
    return i_liquidacion

class LiquidacionMethodTest(TestCase):

    def test_salario_minimo_anio_correcto(self):
        """
        prove that salario minimo is in the correct year, and is calculated propertly
        :return:
        """
        create_salario_minimo()
        a_fecha_inicio = date(now().year-1,1,1)
        a_fecha_liquidacion = date(now().year-1,3,3)
        instance = Liquidacion(fecha_inicio=a_fecha_inicio, fecha_liquidacion=a_fecha_liquidacion)
        self.assertEqual(instance.salario_minimo.pk, now().year-1)

    def test_fecha_inicio_posterior_a_fecha_liquidacion(self):
        """
        The start date cann`t be greater than  the liquidation date we must pass this test
        """
        create_salario_minimo()
        a_fecha_inicio = now()
        a_fecha_liquidacion = a_fecha_inicio - timedelta(days=30)
        instancia_mala = Liquidacion(fecha_inicio=a_fecha_inicio, fecha_liquidacion=a_fecha_liquidacion)
        self.assertEqual(instancia_mala.dias_trabajados_anual, 0)
        self.assertEqual(instancia_mala.dias_trabajados_primer_semestre, 0)
        self.assertEqual(instancia_mala.dias_trabajados_segundo_semestre, 0)

    def test_liquidacion_solo_primer_semestre(self):
        """
        The liquidacion in first semester cannot calculate second semester's prima
        it creates a Liquidacion Object that is in the first semester and try various assertions
        :return: return assertion if Prima 2nd semester is 0 and first semester is ok
        """

        create_salario_minimo()
        a_fecha_inicio= date(now().year, 1, 1)
        a_fecha_liquidacion = date(now().year, 5, 30)
        liquidacion_primer_s = Liquidacion(fecha_inicio=a_fecha_inicio,
                                           fecha_liquidacion=a_fecha_liquidacion)
        self.assertGreater(liquidacion_primer_s.pago_prima_junio, 0, "prima primer semestre es menor o igual que cero")
        self.assertEqual(liquidacion_primer_s.pago_prima_diciembre,0,"prima de segundo semestre no es igual a cero")
        self.assertAlmostEqual(liquidacion_primer_s.pago_prima_junio, BASE_CESANTIAS_PRIMA * 5/12, 2,
                         "el calculo de la prima de julio no corresponde")
        self.assertEqual(liquidacion_primer_s.dias_trabajados_anual, 150, "los dias no suman 150")
        self.assertEqual(liquidacion_primer_s.dias_trabajados_anual,
                         liquidacion_primer_s.dias_trabajados_primer_semestre + liquidacion_primer_s.dias_trabajados_segundo_semestre,
                         "el total de los dias no es igual a la suma de dias de los semestres")
        self.assertAlmostEqual(liquidacion_primer_s.pago_cesantias,BASE_CESANTIAS_PRIMA * 5/12, 2,
                               "el calculo de cesantias no corresponde")
        self.assertAlmostEqual(liquidacion_primer_s.pago_intereses_cesantias,
                               liquidacion_primer_s.pago_cesantias * 0.12 * 5/12, 2,
                               "el calculo de los intereses a las cesantias no corresponde")
        self.assertAlmostEqual(liquidacion_primer_s.pago_vacaciones, 1000000*5/24,
                               2, "el calculo de las vacaciones no corresponde")
        self.assertEqual(liquidacion_primer_s.pago_indemnizacion, 0, "se esta calculando indemnizacion por defecto")
        self.assertEqual(liquidacion_primer_s.pago_indemnizacion_moratoria, 0, "se esta calculando mora por defecto")
        self.assertEqual(liquidacion_primer_s.pago_indemnizacion_cesantias, 0, "se esta calculando indemnizacion por cesantias")


    def test_liquidacion_solo_segundo_semestre(self):
        """
        The liquidacion in second semmester cannot calculate second semester's prima
        creates a Liquidacion Object in the second semester an try various assertions
        asserts if  prima junio is zero, prima diciembre is half average salary and worked days are 180
        :return: nothinng
        """
        create_salario_minimo()
        a_fecha_inicio = date(now().year, 7, 1)
        a_fecha_liquidacion = date(now().year, 11, 30)
        liquidacion_segundo_s = Liquidacion(fecha_inicio=a_fecha_inicio,
                                            fecha_liquidacion=a_fecha_liquidacion)
        self.assertEqual(liquidacion_segundo_s.pago_prima_junio, 0, "prima primer semestre no es igual a cero")
        self.assertGreater(liquidacion_segundo_s.pago_prima_diciembre, 0, "prima segundo semestre es menor o igual a cero")
        self.assertAlmostEqual(liquidacion_segundo_s.pago_prima_diciembre, BASE_CESANTIAS_PRIMA * 5/12, 2,
                         "el calculo de la prima de diciembre no corresponde a 15 dias de salario")
        self.assertEqual(liquidacion_segundo_s.dias_trabajados_anual, 150, "los dias no suman 150")
        self.assertEqual(liquidacion_segundo_s.dias_trabajados_anual,
                         liquidacion_segundo_s.dias_trabajados_primer_semestre + liquidacion_segundo_s.dias_trabajados_segundo_semestre,
                         "el total de los dias no es igual a la suma de dias de los semestres")
        self.assertAlmostEqual(liquidacion_segundo_s.pago_cesantias, BASE_CESANTIAS_PRIMA * 5 / 12, 2,
                               "el calculo de cesantias no corresponde")
        self.assertAlmostEqual(liquidacion_segundo_s.pago_intereses_cesantias,
                               liquidacion_segundo_s.pago_cesantias * 0.12 * 5 / 12, 2,
                               "el calculo de los intereses a las cesantias no corresponde")
        self.assertAlmostEqual(liquidacion_segundo_s.pago_vacaciones, 1000000 * 5 / 24,
                               2, "el calculo de las vacaciones no corresponde")
        self.assertEqual(liquidacion_segundo_s.pago_indemnizacion, 0, "se esta calculando indemnizacion por defecto")
        self.assertEqual(liquidacion_segundo_s.pago_indemnizacion_moratoria, 0, "se esta calculando mora por defecto")
        self.assertEqual(liquidacion_segundo_s.pago_indemnizacion_cesantias, 0,
                         "se esta calculando indemnizacion por cesantias")

    def test_liquidacion_en_mitad_anio(self):
        """
        The liqudacion at half year must calculate both prima and worked days
        :return: nothing
        """
        create_salario_minimo()
        a_fecha_inicio = date(now().year, 2, 1)
        a_fecha_liquidacion = date(now().year, 11, 30)
        liquidacion_mitad_s = Liquidacion(fecha_inicio=a_fecha_inicio, fecha_liquidacion=a_fecha_liquidacion)
        self.assertGreater(liquidacion_mitad_s.pago_prima_junio, 0, "prima primer semestre es cero o negativa")
        self.assertGreater(liquidacion_mitad_s.pago_prima_diciembre, 0, "prima segundo semestre es cero o negativa")
        self.assertAlmostEqual(liquidacion_mitad_s.pago_prima_junio, BASE_CESANTIAS_PRIMA * 5 / 12,places=2,
                               msg="el calculo de la prima de junio no corresponde a 15 dias de salario")
        self.assertAlmostEqual(liquidacion_mitad_s.pago_prima_diciembre, BASE_CESANTIAS_PRIMA * 5 / 12, places=2,
                               msg="el calculo de la prima de diciembre no corresponde a 15 dias de salario")
        self.assertEqual(liquidacion_mitad_s.dias_trabajados_anual, 300, "los dias no suman 300")
        self.assertEqual(liquidacion_mitad_s.dias_trabajados_anual,
                         liquidacion_mitad_s.dias_trabajados_primer_semestre + liquidacion_mitad_s.dias_trabajados_segundo_semestre,
                         "el total de dias no coincide con la suma de los dias de cada semestre")
        self.assertAlmostEqual(liquidacion_mitad_s.pago_cesantias, BASE_CESANTIAS_PRIMA * 10 / 12, 2,
                               "el calculo de cesantias no corresponde")
        self.assertAlmostEqual(liquidacion_mitad_s.pago_intereses_cesantias,
                               liquidacion_mitad_s.pago_cesantias * 0.12 * 10 / 12, 2,
                               "el calculo de los intereses a las cesantias no corresponde")
        self.assertAlmostEqual(liquidacion_mitad_s.pago_vacaciones, 1000000 * 10 / 24,
                               2, "el calculo de las vacaciones no corresponde")
        self.assertEqual(liquidacion_mitad_s.pago_indemnizacion, 0, "se esta calculando indemnizacion por defecto")
        self.assertEqual(liquidacion_mitad_s.pago_indemnizacion_moratoria, 0, "se esta calculando mora por defecto")
        self.assertEqual(liquidacion_mitad_s.pago_indemnizacion_cesantias, 0,
                         "se esta calculando indemnizacion por cesantias")

    def test_liquidacion_sin_justa_causa_actual_menos_de_anio_indefinido(self):
        """
        Takes one instance that have liquidacion with the law of 1993 and prove all calculations
        :return:
        """
        create_salario_minimo()
        a_fecha_liquidacion = date(now().year, 12, 31)
        a_fecha_inicio = date(now().year, 1, 1)
        i_liquid_sin_justa_causa = Liquidacion(causal_terminacion=Liquidacion.SIN_JUSTA_CAUSA,
                                               fecha_inicio=a_fecha_inicio, fecha_liquidacion=a_fecha_liquidacion,
                                               clase_contrato=Liquidacion.INDEFINIDO)
        self.assertEqual(i_liquid_sin_justa_causa.dias_trabajados_anual, 360,
                         """No se estan calculando bien lod dias laborados cuando hay despido sin justa causa""")
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_prima_junio, BASE_CESANTIAS_PRIMA * 6 / 12, 2,
                               """la prima de julio no se esta calculando correctamente sin justa causa """)
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_prima_diciembre, BASE_CESANTIAS_PRIMA * 6 / 12, 2,
                               """la prima de julio no se esta calculando correctamente sin justa causa """)
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_cesantias, BASE_CESANTIAS_PRIMA, 2,
                               """Las cesantias no se calculan bien cuando hay despido sin justa causa""")
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_vacaciones, 1000000 *12/24, 2,
                               """Las vacaciones no se calcullan bien cuando hay despido sin justa causa""")
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_indemnizacion, 1000000, 2,
                               """La liquidacion no se esta calculando correctamente sin justa causa""")
        self.assertAlmostEqual(i_liquid_sin_justa_causa.subtotal_indemnizaciones,
                               i_liquid_sin_justa_causa.pago_indemnizacion, 2,
                               """el total de liquidacion no  es igual a la indemnizacion""")

    def test_liquidacion_sin_justa_causa_actual_mas_de_un_anio_indefinited(self):
        """
        Takes one instance that have liquidacion with the law of 1993 and prove all calculations in the case it
        has justification for the end of the contract
        :return:
        """
        create_salario_minimo()
        a_fecha_liquidacion = date(now().year, 12, 31)
        a_fecha_inicio = date(now().year-1, 1, 1)
        i_liquid_sin_justa_causa = Liquidacion(causal_terminacion=Liquidacion.SIN_JUSTA_CAUSA,
                                               fecha_inicio=a_fecha_inicio, fecha_liquidacion=a_fecha_liquidacion,
                                               clase_contrato=Liquidacion.INDEFINIDO)
        self.assertEqual(i_liquid_sin_justa_causa.dias_trabajados_anual, 360,
                         """No se estan calculando bien lod dias laborados cuando hay despido sin justa causa""")
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_prima_junio, BASE_CESANTIAS_PRIMA * 6 / 12, 2,
                               """la prima de julio no se esta calculando correctamente sin justa causa """)
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_prima_diciembre, BASE_CESANTIAS_PRIMA * 6 / 12, 2,
                               """la prima de julio no se esta calculando correctamente sin justa causa """)
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_cesantias, BASE_CESANTIAS_PRIMA, 2,
                               """Las cesantias no se calculan bien cuando hay despido sin justa causa""")
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_vacaciones, 1000000 *12/24, 2,
                               """Las vacaciones no se calcullan bien cuando hay despido sin justa causa""")
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_indemnizacion, 1000000 *50/30, 2,
                               """La liquidacion no se esta calculando correctamente sin justa causa""")
        self.assertAlmostEqual(i_liquid_sin_justa_causa.subtotal_indemnizaciones,
                               i_liquid_sin_justa_causa.pago_indemnizacion, 2,
                               """el total de liquidacion no  es igual a la indemnizacion""")

    def test_liquidacion_sin_justa_causa_actual_termino_fijo(self):
        """
        Takes one instance that have liquidacion with the law of 1993 and prove all calculations in the case it
        has justification for the end of the contract with a fixed term contract
        :return:
        """
        create_salario_minimo()
        a_fecha_liquidacion = date(now().year, 12, 31)
        a_fecha_inicio = date(now().year-1, 1, 1)
        i_liquid_sin_justa_causa = Liquidacion(causal_terminacion=Liquidacion.SIN_JUSTA_CAUSA,
                                               fecha_inicio=a_fecha_inicio, fecha_liquidacion=a_fecha_liquidacion,
                                               clase_contrato=Liquidacion.FIJO)
        self.assertEqual(i_liquid_sin_justa_causa.dias_trabajados_anual, 360,
                         """No se estan calculando bien los dias laborados cuando hay despido sin justa causa""")
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_prima_junio, BASE_CESANTIAS_PRIMA * 6 / 12, 2,
                               """la prima de julio no se esta calculando correctamente sin justa causa """)
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_prima_diciembre, BASE_CESANTIAS_PRIMA * 6 / 12, 2,
                               """la prima de julio no se esta calculando correctamente sin justa causa """)
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_cesantias, BASE_CESANTIAS_PRIMA, 2,
                               """Las cesantias no se calculan bien cuando hay despido sin justa causa""")
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_vacaciones, 1000000 *12/24, 2,
                               """Las vacaciones no se calcullan bien cuando hay despido sin justa causa""")
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_indemnizacion, 1000000 *15/30, 2,
                               """La liquidacion no se esta calculando correctamente sin justa causa""")
        self.assertAlmostEqual(i_liquid_sin_justa_causa.subtotal_indemnizaciones,
                               i_liquid_sin_justa_causa.pago_indemnizacion, 2,
                               """el total de liquidacion no  es igual a la indemnizacion""")

        i_liquid_sin_justa_causa.fecha_finalizacion = date(now().year+1, 12, 29).date()
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_indemnizacion, 1000000 * 360/30, 2,
                               """La liquidacion no se esta calculando correctamente sin justa causa""")

########################################################################################################################
#################################SALARIOS POR DIAS EMP_DOMESTICO############################################################
########################################################################################################################

    def test_liquidacion_solo_primer_semestre_empleado_domestico(self):
        """
        The liquidacion in first semester cannot calculate second semester's prima and its home maid personal
        it creates a Liquidacion Object that is in the first semester and try various assertions
        :return: return assertion if Prima 2nd semester is 0 and first semester is ok
        """

        create_salario_minimo()
        a_fecha_inicio= date(now().year, 1, 1)
        a_fecha_liquidacion = date(now().year, 5, 30)
        a_tipo_salario = Liquidacion.EMP_DOMESTICO
        a_dias_semanales = 1
        liquidacion_primer_s = Liquidacion(fecha_inicio=a_fecha_inicio,
                                           fecha_liquidacion=a_fecha_liquidacion,
                                           tipo_salario=a_tipo_salario,
                                           dias_semanales=a_dias_semanales)
        self.assertGreater(liquidacion_primer_s.pago_prima_junio, 0, "prima primer semestre es menor o igual que cero")
        self.assertEqual(liquidacion_primer_s.pago_prima_diciembre,0,"prima de segundo semestre no es igual a cero")
        self.assertAlmostEqual(liquidacion_primer_s.pago_prima_junio, (BASE_CESANTIAS_PRIMA*1/7) * 5/12, 2,
                         "el calculo de la prima de julio no corresponde")
        self.assertEqual(liquidacion_primer_s.dias_trabajados_anual, 150, "los dias no suman 150")
        self.assertEqual(liquidacion_primer_s.dias_trabajados_anual,
                         liquidacion_primer_s.dias_trabajados_primer_semestre + liquidacion_primer_s.dias_trabajados_segundo_semestre,
                         "el total de los dias no es igual a la suma de dias de los semestres")
        self.assertAlmostEqual(liquidacion_primer_s.pago_cesantias,(BASE_CESANTIAS_PRIMA*a_dias_semanales/7) * 5/12, 2,
                               "el calculo de cesantias no corresponde")
        self.assertAlmostEqual(liquidacion_primer_s.pago_intereses_cesantias,
                               liquidacion_primer_s.pago_cesantias * 0.12 * 5/12, 2,
                               "el calculo de los intereses a las cesantias no corresponde")
        self.assertAlmostEqual(liquidacion_primer_s.pago_vacaciones, (1000000*1/7)*5/24,
                               2, "el calculo de las vacaciones no corresponde")
        self.assertEqual(liquidacion_primer_s.pago_indemnizacion, 0, "se esta calculando indemnizacion por defecto")
        self.assertEqual(liquidacion_primer_s.pago_indemnizacion_moratoria, 0, "se esta calculando mora por defecto")
        self.assertEqual(liquidacion_primer_s.pago_indemnizacion_cesantias, 0, "se esta calculando indemnizacion por cesantias")


    def test_liquidacion_solo_segundo_semestre_servicio_domestico(self):
        """
        The liquidacion in second semmester cannot calculate second semester's prima
        creates a Liquidacion Object in the second semester an try various assertions
        asserts if  prima junio is zero, prima diciembre is half average salary and worked days are 180
        :return: nothinng
        """
        create_salario_minimo()
        a_fecha_inicio = date(now().year, 7, 1)
        a_fecha_liquidacion = date(now().year, 11, 30)
        a_tipo_salario = Liquidacion.EMP_DOMESTICO
        a_dias_semanales = 1
        liquidacion_segundo_s = Liquidacion(fecha_inicio=a_fecha_inicio,
                                            fecha_liquidacion=a_fecha_liquidacion,
                                            tipo_salario=a_tipo_salario,
                                            dias_semanales=a_dias_semanales)
        self.assertEqual(liquidacion_segundo_s.pago_prima_junio, 0, "prima primer semestre no es igual a cero")
        self.assertGreater(liquidacion_segundo_s.pago_prima_diciembre, 0, "prima segundo semestre es menor o igual a cero")
        self.assertAlmostEqual(liquidacion_segundo_s.pago_prima_diciembre, (BASE_CESANTIAS_PRIMA * a_dias_semanales/7) * 5/12, 2,
                         "el calculo de la prima de diciembre no corresponde a 15 dias de salario")
        self.assertEqual(liquidacion_segundo_s.dias_trabajados_anual, 150, "los dias no suman 150")
        self.assertEqual(liquidacion_segundo_s.dias_trabajados_anual,
                         liquidacion_segundo_s.dias_trabajados_primer_semestre + liquidacion_segundo_s.dias_trabajados_segundo_semestre,
                         "el total de los dias no es igual a la suma de dias de los semestres")
        self.assertAlmostEqual(liquidacion_segundo_s.pago_cesantias, (BASE_CESANTIAS_PRIMA * a_dias_semanales/7) * 5 / 12, 2,
                               "el calculo de cesantias no corresponde")
        self.assertAlmostEqual(liquidacion_segundo_s.pago_intereses_cesantias,
                               liquidacion_segundo_s.pago_cesantias * 0.12 * 5 / 12, 2,
                               "el calculo de los intereses a las cesantias no corresponde")
        self.assertAlmostEqual(liquidacion_segundo_s.pago_vacaciones, (1000000 * a_dias_semanales/7) * 5 / 24,
                               2, "el calculo de las vacaciones no corresponde")
        self.assertEqual(liquidacion_segundo_s.pago_indemnizacion, 0, "se esta calculando indemnizacion por defecto")
        self.assertEqual(liquidacion_segundo_s.pago_indemnizacion_moratoria, 0, "se esta calculando mora por defecto")
        self.assertEqual(liquidacion_segundo_s.pago_indemnizacion_cesantias, 0,
                         "se esta calculando indemnizacion por cesantias")

    def test_liquidacion_en_mitad_anio_servicio_domestico(self):
        """
        The liqudacion at half year must calculate both prima and worked days
        :return: nothing
        """
        create_salario_minimo()
        a_fecha_inicio = date(now().year, 2, 1)
        a_fecha_liquidacion = date(now().year, 11, 30)
        a_tipo_salario = Liquidacion.EMP_DOMESTICO
        a_dias_semanales = 1
        liquidacion_mitad_s = Liquidacion(fecha_inicio=a_fecha_inicio, fecha_liquidacion=a_fecha_liquidacion,
                                          tipo_salario=a_tipo_salario, dias_semanales=a_dias_semanales)
        self.assertGreater(liquidacion_mitad_s.pago_prima_junio, 0, "prima primer semestre es cero o negativa")
        self.assertGreater(liquidacion_mitad_s.pago_prima_diciembre, 0, "prima segundo semestre es cero o negativa")
        self.assertAlmostEqual(liquidacion_mitad_s.pago_prima_junio, (BASE_CESANTIAS_PRIMA*a_dias_semanales/7) * 5 / 12,places=2,
                               msg="el calculo de la prima de junio no corresponde a 15 dias de salario")
        self.assertAlmostEqual(liquidacion_mitad_s.pago_prima_diciembre, (BASE_CESANTIAS_PRIMA*a_dias_semanales/7) * 5 / 12, places=2,
                               msg="el calculo de la prima de diciembre no corresponde a 15 dias de salario")
        self.assertEqual(liquidacion_mitad_s.dias_trabajados_anual, 300, "los dias no suman 300")
        self.assertEqual(liquidacion_mitad_s.dias_trabajados_anual,
                         liquidacion_mitad_s.dias_trabajados_primer_semestre + liquidacion_mitad_s.dias_trabajados_segundo_semestre,
                         "el total de dias no coincide con la suma de los dias de cada semestre")
        self.assertAlmostEqual(liquidacion_mitad_s.pago_cesantias, (BASE_CESANTIAS_PRIMA*a_dias_semanales/7) * 10 / 12, 2,
                               "el calculo de cesantias no corresponde")
        self.assertAlmostEqual(liquidacion_mitad_s.pago_intereses_cesantias,
                               liquidacion_mitad_s.pago_cesantias * 0.12 * 10 / 12, 2,
                               "el calculo de los intereses a las cesantias no corresponde")
        self.assertAlmostEqual(liquidacion_mitad_s.pago_vacaciones, (1000000*a_dias_semanales/7) * 10 / 24,
                               2, "el calculo de las vacaciones no corresponde")
        self.assertEqual(liquidacion_mitad_s.pago_indemnizacion, 0, "se esta calculando indemnizacion por defecto")
        self.assertEqual(liquidacion_mitad_s.pago_indemnizacion_moratoria, 0, "se esta calculando mora por defecto")
        self.assertEqual(liquidacion_mitad_s.pago_indemnizacion_cesantias, 0,
                         "se esta calculando indemnizacion por cesantias")

    def test_liquidacion_sin_justa_causa_actual_menos_de_anio_indefinido_empleado_domestico(self):
        """
        Takes one instance that have liquidacion with the law of 1993 and prove all calculations
        :return:
        """
        create_salario_minimo()
        a_fecha_liquidacion = date(now().year, 12, 31)
        a_fecha_inicio = date(now().year, 1, 1)
        a_tipo_salario = Liquidacion.EMP_DOMESTICO
        a_dias_semanales = 1
        i_liquid_sin_justa_causa = Liquidacion(causal_terminacion=Liquidacion.SIN_JUSTA_CAUSA,
                                               fecha_inicio=a_fecha_inicio, fecha_liquidacion=a_fecha_liquidacion,
                                               clase_contrato=Liquidacion.INDEFINIDO, dias_semanales=a_dias_semanales,
                                               tipo_salario=a_tipo_salario)
        self.assertEqual(i_liquid_sin_justa_causa.dias_trabajados_anual, 360,
                         """No se estan calculando bien lod dias laborados cuando hay despido sin justa causa""")
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_prima_junio, (BASE_CESANTIAS_PRIMA*a_dias_semanales/7)* 6 / 12, 2,
                               """la prima de julio no se esta calculando correctamente sin justa causa """)
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_prima_diciembre, (BASE_CESANTIAS_PRIMA*a_dias_semanales/7) * 6 / 12, 2,
                               """la prima de julio no se esta calculando correctamente sin justa causa """)
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_cesantias, (BASE_CESANTIAS_PRIMA*a_dias_semanales/7), 2,
                               """Las cesantias no se calculan bien cuando hay despido sin justa causa""")
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_vacaciones, (1000000*a_dias_semanales/7) *12/24, 2,
                               """Las vacaciones no se calcullan bien cuando hay despido sin justa causa""")
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_indemnizacion, (1000000*a_dias_semanales/7), 2,
                               """La liquidacion no se esta calculando correctamente sin justa causa""")
        self.assertAlmostEqual(i_liquid_sin_justa_causa.subtotal_indemnizaciones,
                               i_liquid_sin_justa_causa.pago_indemnizacion, 2,
                               """el total de liquidacion no  es igual a la indemnizacion""")

    def test_liquidacion_sin_justa_causa_actual_mas_de_un_anio_indefinido_empleado_domestico(self):
        """
        Takes one instance that have liquidacion with the law of 1993 and prove all calculations in the case it
        has justification for the end of the contract
        :return:
        """
        create_salario_minimo()
        a_fecha_liquidacion = date(now().year, 12, 31)
        a_fecha_inicio = date(now().year-1, 1, 1)
        a_tipo_salario = Liquidacion.EMP_DOMESTICO
        a_dias_semanales = 1
        i_liquid_sin_justa_causa = Liquidacion(causal_terminacion=Liquidacion.SIN_JUSTA_CAUSA,
                                               fecha_inicio=a_fecha_inicio, fecha_liquidacion=a_fecha_liquidacion,
                                               clase_contrato=Liquidacion.INDEFINIDO, dias_semanales=a_dias_semanales,
                                               tipo_salario=a_tipo_salario)
        self.assertEqual(i_liquid_sin_justa_causa.dias_trabajados_anual, 360,
                         """No se estan calculando bien lod dias laborados cuando hay despido sin justa causa""")
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_prima_junio, (BASE_CESANTIAS_PRIMA*a_dias_semanales/7)* 6 / 12, 2,
                               """la prima de julio no se esta calculando correctamente sin justa causa """)
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_prima_diciembre, (BASE_CESANTIAS_PRIMA*a_dias_semanales/7) * 6 / 12, 2,
                               """la prima de julio no se esta calculando correctamente sin justa causa """)
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_cesantias, (BASE_CESANTIAS_PRIMA*a_dias_semanales/7), 2,
                               """Las cesantias no se calculan bien cuando hay despido sin justa causa""")
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_vacaciones, (1000000*a_dias_semanales/7) *12/24, 2,
                               """Las vacaciones no se calcullan bien cuando hay despido sin justa causa""")
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_indemnizacion, (1000000*a_dias_semanales/7) *50/30, 2,
                               """La liquidacion no se esta calculando correctamente sin justa causa""")
        self.assertAlmostEqual(i_liquid_sin_justa_causa.subtotal_indemnizaciones,
                               i_liquid_sin_justa_causa.pago_indemnizacion, 2,
                               """el total de liquidacion no  es igual a la indemnizacion""")

    def test_liquidacion_sin_justa_causa_actual_termino_fijo(self):
        """
        Takes one instance that have liquidacion with the law of 1993 and prove all calculations in the case it
        has justification for the end of the contract with a fixed term contract
        :return:
        """
        create_salario_minimo()
        a_fecha_liquidacion = date(now().year, 12, 31)
        a_fecha_inicio = date(now().year-1, 1, 1)
        a_tipo_salario = Liquidacion.EMP_DOMESTICO
        a_dias_semanales = 1
        i_liquid_sin_justa_causa = Liquidacion(causal_terminacion=Liquidacion.SIN_JUSTA_CAUSA,
                                               fecha_inicio=a_fecha_inicio, fecha_liquidacion=a_fecha_liquidacion,
                                               clase_contrato=Liquidacion.FIJO, tipo_salario=a_tipo_salario,
                                               dias_semanales=a_dias_semanales)
        self.assertEqual(i_liquid_sin_justa_causa.dias_trabajados_anual, 360,
                         """No se estan calculando bien los dias laborados cuando hay despido sin justa causa""")
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_prima_junio, (BASE_CESANTIAS_PRIMA*a_dias_semanales/7)* 6 / 12, 2,
                               """la prima de julio no se esta calculando correctamente sin justa causa """)
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_prima_diciembre, (BASE_CESANTIAS_PRIMA*a_dias_semanales/7) * 6 / 12, 2,
                               """la prima de julio no se esta calculando correctamente sin justa causa """)
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_cesantias, (BASE_CESANTIAS_PRIMA*a_dias_semanales/7), 2,
                               """Las cesantias no se calculan bien cuando hay despido sin justa causa""")
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_vacaciones, (1000000*a_dias_semanales/7) *12/24, 2,
                               """Las vacaciones no se calcullan bien cuando hay despido sin justa causa""")
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_indemnizacion, (1000000*1/7) *15/30, 2,
                               """La liquidacion no se esta calculando correctamente sin justa causa""")
        self.assertAlmostEqual(i_liquid_sin_justa_causa.subtotal_indemnizaciones,
                               i_liquid_sin_justa_causa.pago_indemnizacion, 2,
                               """el total de liquidacion no  es igual a la indemnizacion""")

        i_liquid_sin_justa_causa.fecha_finalizacion = date(now().year+1, 12, 29)
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_indemnizacion, (1000000*a_dias_semanales/7) * 360/30, 2,
                               """La liquidacion no se esta calculando correctamente sin justa causa""")


########################################################################################################################
#################################SALARIOS EMPLEADOS DE CONSTRUCCION############################################################
########################################################################################################################

    def test_liquidacion_solo_primer_semestre_empleado_construccion(self):
        """
        The liquidacion in first semester cannot calculate second semester's prima and its construction personal
        it creates a Liquidacion Object that is in the first semester and try various assertions
        :return: return assertion if Prima 2nd semester is 0 and first semester is ok
        """

        create_salario_minimo()
        a_fecha_inicio= date(now().year, 1, 1)
        a_fecha_liquidacion = date(now().year, 5, 30)
        a_tipo_salario = Liquidacion.EMP_CONSTRUCCION
        a_aplica_art_310 = True
        a_dias_semanales = 7
        liquidacion_primer_s = Liquidacion(fecha_inicio=a_fecha_inicio,
                                           fecha_liquidacion=a_fecha_liquidacion,
                                           tipo_salario=a_tipo_salario, aplica_art_310=a_aplica_art_310,
                                           dias_semanales=a_dias_semanales)
        self.assertGreater(liquidacion_primer_s.pago_prima_junio, 0, "prima primer semestre es menor o igual que cero")
        self.assertEqual(liquidacion_primer_s.pago_prima_diciembre,0,"prima de segundo semestre no es igual a cero")
        self.assertAlmostEqual(liquidacion_primer_s.pago_prima_junio, (BASE_CESANTIAS_PRIMA) * 5/12, 2,
                         "el calculo de la prima de julio no corresponde")
        self.assertEqual(liquidacion_primer_s.dias_trabajados_anual, 150, "los dias no suman 150")
        self.assertEqual(liquidacion_primer_s.dias_trabajados_anual,
                         liquidacion_primer_s.dias_trabajados_primer_semestre + liquidacion_primer_s.dias_trabajados_segundo_semestre,
                         "el total de los dias no es igual a la suma de dias de los semestres")
        self.assertAlmostEqual(liquidacion_primer_s.pago_cesantias,(BASE_CESANTIAS_PRIMA*a_dias_semanales/7) * 1/2, 2,
                               "el calculo de cesantias no corresponde")
        self.assertAlmostEqual(liquidacion_primer_s.pago_intereses_cesantias,
                               liquidacion_primer_s.pago_cesantias * 0.12 * 5/12, 2,
                               "el calculo de los intereses a las cesantias no corresponde")
        self.assertAlmostEqual(liquidacion_primer_s.pago_vacaciones, (1000000*7/7)*5/24,
                               2, "el calculo de las vacaciones no corresponde")
        self.assertEqual(liquidacion_primer_s.pago_indemnizacion, 0, "se esta calculando indemnizacion por defecto")
        self.assertEqual(liquidacion_primer_s.pago_indemnizacion_moratoria, 0, "se esta calculando mora por defecto")
        self.assertEqual(liquidacion_primer_s.pago_indemnizacion_cesantias, 0, "se esta calculando indemnizacion por cesantias")


    def test_liquidacion_solo_segundo_semestre_empleado_construccion(self):
        """
        The liquidacion in second semmester cannot calculate second semester's prima
        creates a Liquidacion Object in the second semester an try various assertions
        asserts if  prima junio is zero, prima diciembre is half average salary and worked days are 180
        :return: nothinng
        """
        create_salario_minimo()
        a_fecha_inicio = date(now().year, 7, 1)
        a_fecha_liquidacion = date(now().year, 11, 30)
        a_tipo_salario = Liquidacion.EMP_CONSTRUCCION
        a_aplica_art_310 = True
        a_dias_semanales = 7
        liquidacion_segundo_s = Liquidacion(fecha_inicio=a_fecha_inicio,
                                            fecha_liquidacion=a_fecha_liquidacion,
                                            tipo_salario=a_tipo_salario, aplica_art_310=a_aplica_art_310,
                                            dias_semanales=a_dias_semanales)
        self.assertEqual(liquidacion_segundo_s.pago_prima_junio, 0, "prima primer semestre no es igual a cero")
        self.assertGreater(liquidacion_segundo_s.pago_prima_diciembre, 0, "prima segundo semestre es menor o igual a cero")
        self.assertAlmostEqual(liquidacion_segundo_s.pago_prima_diciembre, (BASE_CESANTIAS_PRIMA * a_dias_semanales/7) * 5/12, 2,
                         "el calculo de la prima de diciembre no corresponde a 15 dias de salario")
        self.assertEqual(liquidacion_segundo_s.dias_trabajados_anual, 150, "los dias no suman 150")
        self.assertEqual(liquidacion_segundo_s.dias_trabajados_anual,
                         liquidacion_segundo_s.dias_trabajados_primer_semestre + liquidacion_segundo_s.dias_trabajados_segundo_semestre,
                         "el total de los dias no es igual a la suma de dias de los semestres")
        self.assertAlmostEqual(liquidacion_segundo_s.pago_cesantias, (BASE_CESANTIAS_PRIMA * a_dias_semanales/7) * 1 / 2, 2,
                               "el calculo de cesantias no corresponde")
        self.assertAlmostEqual(liquidacion_segundo_s.pago_intereses_cesantias,
                               liquidacion_segundo_s.pago_cesantias * 0.12 * 5 / 12, 2,
                               "el calculo de los intereses a las cesantias no corresponde")
        self.assertAlmostEqual(liquidacion_segundo_s.pago_vacaciones, (1000000 * a_dias_semanales/7) * 5 / 24,
                               2, "el calculo de las vacaciones no corresponde")
        self.assertEqual(liquidacion_segundo_s.pago_indemnizacion, 0, "se esta calculando indemnizacion por defecto")
        self.assertEqual(liquidacion_segundo_s.pago_indemnizacion_moratoria, 0, "se esta calculando mora por defecto")
        self.assertEqual(liquidacion_segundo_s.pago_indemnizacion_cesantias, 0,
                         "se esta calculando indemnizacion por cesantias")

    def test_liquidacion_en_mitad_anio_empleado_construccion(self):
        """
        The liqudacion at half year must calculate both prima and worked days
        :return: nothing
        """
        create_salario_minimo()
        a_fecha_inicio = date(now().year, 2, 1)
        a_fecha_liquidacion = date(now().year, 11, 30)
        a_tipo_salario = Liquidacion.EMP_CONSTRUCCION
        a_aplica_art_310 = True
        a_dias_semanales = 7
        liquidacion_mitad_s = Liquidacion(fecha_inicio=a_fecha_inicio, fecha_liquidacion=a_fecha_liquidacion,
                                          tipo_salario=a_tipo_salario, dias_semanales=a_dias_semanales,
                                          aplica_art_310=a_aplica_art_310)
        self.assertGreater(liquidacion_mitad_s.pago_prima_junio, 0, "prima primer semestre es cero o negativa")
        self.assertGreater(liquidacion_mitad_s.pago_prima_diciembre, 0, "prima segundo semestre es cero o negativa")
        self.assertAlmostEqual(liquidacion_mitad_s.pago_prima_junio, (BASE_CESANTIAS_PRIMA*a_dias_semanales/7) * 5 / 12,places=2,
                               msg="el calculo de la prima de junio no corresponde a 15 dias de salario")
        self.assertAlmostEqual(liquidacion_mitad_s.pago_prima_diciembre, (BASE_CESANTIAS_PRIMA*a_dias_semanales/7) * 5 / 12, places=2,
                               msg="el calculo de la prima de diciembre no corresponde a 15 dias de salario")
        self.assertEqual(liquidacion_mitad_s.dias_trabajados_anual, 300, "los dias no suman 300")
        self.assertEqual(liquidacion_mitad_s.dias_trabajados_anual,
                         liquidacion_mitad_s.dias_trabajados_primer_semestre + liquidacion_mitad_s.dias_trabajados_segundo_semestre,
                         "el total de dias no coincide con la suma de los dias de cada semestre")
        self.assertAlmostEqual(liquidacion_mitad_s.pago_cesantias, (BASE_CESANTIAS_PRIMA*a_dias_semanales/7) * 1 , 2,
                               "el calculo de cesantias no corresponde")
        self.assertAlmostEqual(liquidacion_mitad_s.pago_intereses_cesantias,
                               liquidacion_mitad_s.pago_cesantias * 0.12 * 10 / 12, 2,
                               "el calculo de los intereses a las cesantias no corresponde")
        self.assertAlmostEqual(liquidacion_mitad_s.pago_vacaciones, (1000000*a_dias_semanales/7) * 10 / 24,
                               2, "el calculo de las vacaciones no corresponde")
        self.assertEqual(liquidacion_mitad_s.pago_indemnizacion, 0, "se esta calculando indemnizacion por defecto")
        self.assertEqual(liquidacion_mitad_s.pago_indemnizacion_moratoria, 0, "se esta calculando mora por defecto")
        self.assertEqual(liquidacion_mitad_s.pago_indemnizacion_cesantias, 0,
                         "se esta calculando indemnizacion por cesantias")

    def test_liquidacion_sin_justa_causa_actual_menos_de_anio_indefinido_empleado_construccion(self):
        """
        Takes one instance that have liquidacion with the law of 1993 and prove all calculations
        :return:
        """
        create_salario_minimo()
        a_fecha_liquidacion = date(now().year, 12, 31)
        a_fecha_inicio = date(now().year, 1, 1)
        a_tipo_salario = Liquidacion.EMP_CONSTRUCCION
        a_aplica_art_310 = True
        a_dias_semanales = 7
        i_liquid_sin_justa_causa = Liquidacion(causal_terminacion=Liquidacion.SIN_JUSTA_CAUSA,
                                               fecha_inicio=a_fecha_inicio, fecha_liquidacion=a_fecha_liquidacion,
                                               clase_contrato=Liquidacion.INDEFINIDO, dias_semanales=a_dias_semanales,
                                               tipo_salario=a_tipo_salario, aplica_art_310=a_aplica_art_310)
        self.assertEqual(i_liquid_sin_justa_causa.dias_trabajados_anual, 360,
                         """No se estan calculando bien lod dias laborados cuando hay despido sin justa causa""")
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_prima_junio, (BASE_CESANTIAS_PRIMA*a_dias_semanales/7)* 6 / 12, 2,
                               """la prima de julio no se esta calculando correctamente sin justa causa """)
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_prima_diciembre, (BASE_CESANTIAS_PRIMA*a_dias_semanales/7) * 6 / 12, 2,
                               """la prima de julio no se esta calculando correctamente sin justa causa """)
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_cesantias, (BASE_CESANTIAS_PRIMA*a_dias_semanales/7) *6/5, 2,
                               """Las cesantias no se calculan bien cuando hay despido sin justa causa""")
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_vacaciones, (1000000*a_dias_semanales/7) *12/24, 2,
                               """Las vacaciones no se calcullan bien cuando hay despido sin justa causa""")
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_indemnizacion, (1000000*a_dias_semanales/7), 2,
                               """La liquidacion no se esta calculando correctamente sin justa causa""")
        self.assertAlmostEqual(i_liquid_sin_justa_causa.subtotal_indemnizaciones,
                               i_liquid_sin_justa_causa.pago_indemnizacion, 2,
                               """el total de liquidacion no  es igual a la indemnizacion""")

    def test_liquidacion_sin_justa_causa_actual_mas_de_un_anio_indefinido_empleado_construccion(self):
        """
        Takes one instance that have liquidacion with the law of 1993 and prove all calculations in the case it
        has justification for the end of the contract
        :return:
        """
        create_salario_minimo()
        a_fecha_liquidacion = date(now().year, 12, 31)
        a_fecha_inicio = date(now().year-1, 1, 1)
        a_tipo_salario = Liquidacion.EMP_CONSTRUCCION
        a_aplica_art_310 = True
        a_dias_semanales = 7
        i_liquid_sin_justa_causa = Liquidacion(causal_terminacion=Liquidacion.SIN_JUSTA_CAUSA,
                                               fecha_inicio=a_fecha_inicio, fecha_liquidacion=a_fecha_liquidacion,
                                               clase_contrato=Liquidacion.INDEFINIDO, dias_semanales=a_dias_semanales,
                                               tipo_salario=a_tipo_salario, aplica_art_310=a_aplica_art_310)
        self.assertEqual(i_liquid_sin_justa_causa.dias_trabajados_anual, 360,
                         """No se estan calculando bien lod dias laborados cuando hay despido sin justa causa""")
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_prima_junio, (BASE_CESANTIAS_PRIMA*a_dias_semanales/7)* 6 / 12, 2,
                               """la prima de julio no se esta calculando correctamente sin justa causa """)
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_prima_diciembre, (BASE_CESANTIAS_PRIMA*a_dias_semanales/7) * 6 / 12, 2,
                               """la prima de julio no se esta calculando correctamente sin justa causa """)
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_cesantias, (BASE_CESANTIAS_PRIMA*a_dias_semanales/7)*12/10, 2,
                               """Las cesantias no se calculan bien cuando hay despido sin justa causa""")
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_vacaciones, (1000000*a_dias_semanales/7) *12/24, 2,
                               """Las vacaciones no se calcullan bien cuando hay despido sin justa causa""")
        self.assertAlmostEqual(i_liquid_sin_justa_causa.pago_indemnizacion, (1000000*a_dias_semanales/7) *50/30, 2,
                               """La liquidacion no se esta calculando correctamente sin justa causa""")
        self.assertAlmostEqual(i_liquid_sin_justa_causa.subtotal_indemnizaciones,
                               i_liquid_sin_justa_causa.pago_indemnizacion, 2,
                               """el total de liquidacion no  es igual a la indemnizacion""")

