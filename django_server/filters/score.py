from url_filter.filtersets import ModelFilterSet

from django_server.models import PostScore


class PostScoreFilter(ModelFilterSet):
    class Meta(object):
        model = PostScore
