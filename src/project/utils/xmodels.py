from functools import singledispatch
from typing import Text

import django
from django.db.models.base import ModelBase
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor
from django.db.models.fields.related_descriptors import ManyToManyDescriptor
from django.db.models.query_utils import DeferredAttribute


@singledispatch
def a(obj) -> Text:
    return str(obj)


@a.register(DeferredAttribute)
def _(obj: DeferredAttribute) -> Text:  # фурычит только с 3.7
    if django.VERSION[0] < 3:  # pragma: no cover
        return obj.field_name
    return obj.field.get_attname()


@a.register(ForwardManyToOneDescriptor)
def _(obj: ForwardManyToOneDescriptor) -> Text:
    return obj.field.name


@a.register(ManyToManyDescriptor)
def _(obj: ManyToManyDescriptor) -> Text:
    return obj.field.name


@a.register(ModelBase)
def _(obj: ModelBase) -> Text:
    return obj._meta.db_table
