import graphene
import test_task_app.graphql.schema


class Query(test_task_app.graphql.schema.Query, graphene.ObjectType):
    pass

class Mutation(test_task_app.graphql.schema.Mutation, graphene.ObjectType):
    pass


# schema = graphene.Schema(query=Query)
schema = graphene.Schema(query=Query, mutation=Mutation)

