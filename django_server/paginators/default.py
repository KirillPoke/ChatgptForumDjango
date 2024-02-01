from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 1000

    def paginate_queryset(self, queryset, request, view=None):
        # if the page param is not provided, do not apply pagination
        if request.query_params.get(self.page_query_param, None) is None:
            return None

        return super().paginate_queryset(queryset, request, view)
