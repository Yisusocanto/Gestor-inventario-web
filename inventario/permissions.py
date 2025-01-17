from django.core.exceptions import PermissionDenied

def user_has_role(user, roles):
    if user.rol not in roles:
        raise PermissionDenied