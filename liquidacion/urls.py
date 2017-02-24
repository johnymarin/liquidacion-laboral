from django.conf.urls import url
from . import views

app_name = 'liquidacion'
urlpatterns=[
    #TODO write the new home url
    #TODO change  the name of the view 'index' for the name 'form'
    # ex: /liquidacion/
    url(r'^$', views.full_form, name='full_form'),
    # ex: /liquidacion/resultados
    url(r'^resultados/$', views.results, name='results'),

]