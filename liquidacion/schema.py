import graphene
from graphene_django.types import DjangoObjectType
from liquidacion.models import Liquidacion

class LiquidacionType(DjangoObjectType):
    class Meta:
        model = Liquidacion
