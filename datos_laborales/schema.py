import graphene
from graphene_django.types import DjangoObjectType
from datos_laborales.models import SalarioMinimo, AporteSalud, AportePension

class SalarioMinimoType(DjangoObjectType):
    class Meta:
        model = SalarioMinimo

class AporteSaludType(DjangoObjectType):
    class Meta:
        model = AporteSalud

class AportePensionType(DjangoObjectType):
    class Meta:
        model = AportePension

class Query(graphene.AbstractType):
    all_salarios = graphene.List(SalarioMinimoType)
    all_aportes_salud = graphene.List(AporteSaludType)
    all_aportes_pension = graphene.List(AportePensionType)

    def resolve_all_salarios(self, args, context, info):
        return SalarioMinimo.objects.all()

    def resolve_all_aportes_salud(self, args, context, info):
        return AporteSalud.objects.all()

    def resolve_all_aportes_pension(self,args, context, info):
        return AportePension.objects.all()

        # We can easily optimize query count in the resolve method
        # return Ingredient.objects.select_related('category').all()

