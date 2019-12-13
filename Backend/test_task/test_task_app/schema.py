import graphene
from graphene_django.types import DjangoObjectType

from .models import *


class OccupationType(DjangoObjectType):
    class Meta:
        model = Occupation


class Query(object):
    all_jobbers = graphene.List(OccupationType)

    def resolve_all_jobbers(self, info, **kwargs):
        return Occupation.objects.all()
