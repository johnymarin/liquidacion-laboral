from django.conf.urls import url
from . import views

app_name = 'liquidacion'
urlpatterns=[
    #TODO write the new home url in a new app
    #TODO change  the name of the view 'index' for the name 'form'
    # ex: /liquidacion/
    url(r'^$', views.full_form, name='full_form'),
    # ex: /liquidacion/termino_fijo
    url(r'^termino_fijo/$', views.full_form, {'p_tipo': 'f_fijo'}, name='termino_fijo_form'),
    # ex: /liquidacion/obra_labor
    url(r'^obra_labor/$', views.full_form, {'p_tipo': 'f_obra'}, name='obra_labor_form'),
    # ex: /liquidacion/termino_indefinido
    url(r'^termino_indefinido/$', views.full_form, {'p_tipo': 'f_indefinido'}, name='termino_indefinido_form'),
    # ex: /liquidacion/dias_servicio
    url(r'^dias_servicio/$', views.full_form, {'p_tipo': 'f_dias'}, name='dias_servicio_form'),
    # ex: /liquidacion/resultados or  /liquidacion/termino_fijo/
    #FIXME this actually accepts any url that ends with resultados, make only accept valids url
    url(r'resultados/$', views.results, name='results'),

]