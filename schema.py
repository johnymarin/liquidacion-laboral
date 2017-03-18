import graphene
import datos_laborales.schema

class Query(datos_laborales.schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more app to our project
    pass

schema = graphene.Schema(query=Query)