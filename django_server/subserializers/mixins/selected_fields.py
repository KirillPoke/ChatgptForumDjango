class SelectedFieldsMixin:
    """
    A mixin that allows a serializer to include only the specified fields in the query_params
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "request" in kwargs["context"]:
            query_param_fields = kwargs["context"]["request"].query_params.get("fields")
            if query_param_fields is not None:
                query_param_fields = query_param_fields.split(",")
                allowed = set(query_param_fields)
                existing = set(self.fields.keys())
                for field_name in existing - allowed:
                    self.fields.pop(field_name)
