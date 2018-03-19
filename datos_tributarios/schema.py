import graphene
from graphene_django.types import DjangoObjectType
from datos_tributarios.models import UnidadValorTributario

class UnidadValorTributarioType(DjangoObjectType):
    class Meta:
        model = UnidadValorTributario

class Query(graphene.AbstractType):
    all_unidades_valor_tributario = graphene.List(UnidadValorTributarioType)

    def resolve_all_unidades_valor_tributario(self, args, context, info):
        return UnidadValorTributario.objects.all()
