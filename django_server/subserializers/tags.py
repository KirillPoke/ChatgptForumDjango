from rest_framework import serializers


class TagListField(serializers.ListField):
    child = serializers.CharField()

    def to_representation(self, data):
        # Use values_list to efficiently fetch only tag names in a single query
        return data.values_list("name", flat=True)
