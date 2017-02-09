from django.conf.urls import url
from . import views

app_name = 'liquidacion'
urlpatterns=[
    # ex: /liquidacion/
    url(r'^$', views.index, name='index'),
    # ex: /liquidacion/resultados
    url(r'^resultados/$', views.results, name='results'),

]