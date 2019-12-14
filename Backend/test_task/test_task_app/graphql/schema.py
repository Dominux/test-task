import graphene
from graphene_django.types import DjangoObjectType

from ..models import *


class OccupationType(DjangoObjectType):
    class Meta:
        model = Occupation


class Query:
    getOccupation = graphene.List(OccupationType, occupationId=graphene.ID(required=True))

    def resolve_getOccupation(self, info, **kwargs):
        model_id = kwargs.get("occupationId", "")
        return Occupation.objects.filter(id=model_id)

    getOccupations = graphene.List(OccupationType)

    def resolve_getOccupations(self, info, **kwargs):
        return Occupation.objects.all()


class OccupationMutation(graphene.Mutation):
    class Arguments:
        name          = graphene.String(required=True)
        companyName   = graphene.String(required=True)
        positionName  = graphene.String(required=True)
        hireDate      = graphene.Date(required=True)
        fireDate      = graphene.Date()
        salary        = graphene.Int(required=True)
        fraction      = graphene.Int(required=True)
        base          = graphene.Int(required=True)
        advance       = graphene.Int(required=True)
        by_hours      = graphene.Boolean(required=True)

        # name: String!,
        # companyName: String!,
        # positionName: String!,
        # hireDate: Date!,
        # fireDate: Date,
        # salary: Int!,
        # fraction: Int!,
        # base: Int!,
        # advance: Int!,
        # by_hours: Boolean!

    occupation = graphene.Field(OccupationType)
    
    def mutate(self, info, name, companyName, positionName, hireDate, salary, fraction, base, advance, by_hours, fireDate=None):
        occupation = Occupation.objects.create(
            name=name, 
            company_name=companyName, 
            position_name=positionName,
            hire_date=hireDate,
            fire_date=fireDate,
            salary=salary,
            fraction=fraction,
            base=base,
            advance=advance,
            by_hours=by_hours
        )

        occupation.name          = name
        occupation.company_name  = companyName
        occupation.position_name = positionName
        occupation.salary        = salary
        occupation.fraction      = fraction
        occupation.base          = base
        occupation.advance       = advance
        occupation.by_hours      = by_hours

        occupation.save()
        return OccupationMutation(occupation=occupation)


class Mutation(graphene.ObjectType):
    addOccupation = OccupationMutation.Field()

