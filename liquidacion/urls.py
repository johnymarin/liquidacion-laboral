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
    # ex: /liquidacion/resultados or  /liquidacion/termino_fijo/
    #FIXME this actually accepts any url that ends with resultados, make only accept valid url
    url(r'resultados/$', views.results, name='results'),

]