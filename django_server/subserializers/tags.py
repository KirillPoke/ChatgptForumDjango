from rest_framework import serializers

from django_server.models import Tag


class TagStringRelatedField(serializers.RelatedField):
    def to_internal_value(self, data):
        return Tag.objects.get_or_create(name=data)[0]
        return Tag.objects.bulk_create(
            (Tag(name=name) for name in data), ignore_conflicts=True
        )

    def to_representation(self, value):
        return str(value)
