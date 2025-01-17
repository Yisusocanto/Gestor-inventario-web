from django.contrib.auth.decorators import user_passes_test
from .permissions import user_has_role

def role_required(roles):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            user_has_role(request.user, roles)
            return view_func(request, *args, **kwargs)
        return user_passes_test(lambda u: u.is_authenticated)(_wrapped_view)
    return decorator