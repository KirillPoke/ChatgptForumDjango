from rest_framework import serializers

from django_server.models import Tag


class TagStringRelatedField(serializers.RelatedField):
    def to_internal_value(self, data):
        return Tag.objects.get_or_create(name=data)[0]

    def to_representation(self, value):
        return str(value)
