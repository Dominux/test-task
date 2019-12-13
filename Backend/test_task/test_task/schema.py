import graphene
import test_task_app.schema


class Query(test_task_app.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
