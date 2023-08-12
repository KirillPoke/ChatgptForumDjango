from rest_framework.permissions import BasePermission

RETRIEVE_METHODS = ['GET', 'HEAD', 'OPTIONS']
CREATE_METHODS = ['POST', 'PUT']
REDACT_DESTROY_METHODS = ['PATCH', 'DELETE']


def handle_retrieve(*args, **kwargs):
    return True


def handle_create(request, *args, **kwargs):
    return request.user.is_authenticated


def handle_redact_destroy(request, view, **kwargs):
    model_id = view.kwargs['pk']
    related_model_instance = view.queryset.get(id=model_id)
    return request.user.is_authenticated and related_model_instance.author == request.user


def handle_request(request, view):
    handlers = {
        **dict.fromkeys(RETRIEVE_METHODS, handle_retrieve),
        **dict.fromkeys(CREATE_METHODS, handle_create),
        **dict.fromkeys(REDACT_DESTROY_METHODS, handle_redact_destroy),
    }
    return handlers.get(request.method, lambda method: False)(request, view)


class ReadOnlyOrOwner(BasePermission):
    """
    The request is authenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return handle_request(request, view)
