"""liquidacionsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from liquidacion.views import home as homeview
from homeapp.views import index as home2indexview
from liquidacion.views import tictactoe as tictactoeview
from liquidacion.views import contact as contactview
from liquidacion.views import terms as termsview
from graphene_django.views import GraphQLView

urlpatterns = [
    # TODO point the root url to a home view in the home app http://grasshopperpebbles.com/django-python/how-to-set-up-a-home-page-with-django/
    url(r'^$', homeview, name="home"),
    url(r'^home2/', home2indexview),
    url(r'^liquidacion/', include('liquidacion.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^graphql', GraphQLView.as_view(graphiql = True)),
    url(r'^tictactoe',tictactoeview , name="tictactoe"),
    url(r'^contact',contactview, name="contact"),
    url(r'^terms',termsview, name="terms"),
]
