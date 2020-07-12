import base64
from functools import wraps
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, REDIRECT_FIELD_NAME
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse


def permission_required(function=None, names=None):
    """Декоратор проверяющший наличие пользователя в определенных группах."""
    def decorator_group(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if names:
                if not any(map(lambda name: request.user.has_perm(name), names)):
                    return HttpResponse(status=403)
            return view_func(request, *args, **kwargs)
        return _wrapped_view

    if function:
        return decorator_group(function)
    return decorator_group


def groups_required(function=None, names=None):
    """Декоратор проверяющший наличие пользователя в определенных группах."""
    def decorator_group(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if names:
                if not any(map(lambda name: request.user.groups.filter(name=name).count(), names)):
                    return HttpResponse(status=403)
            return view_func(request, *args, **kwargs)
        return _wrapped_view

    if function:
        return decorator_group(function)
    return decorator_group


def basicauth(view_func):
    """Декоратор реализующий HTTP Basic AUTH."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'HTTP_AUTHORIZATION' in request.META:
            auth = request.META['HTTP_AUTHORIZATION'].split()
            if len(auth) == 2:
                if auth[0].lower() == 'basic':
                    token = base64.b64decode(auth[1].encode('ascii'))
                    username, password = token.decode('utf-8').split(':')
                    user = authenticate(username=username, password=password)
                    if user is not None and user.is_active:
                        request.user = user
                        return view_func(request, *args, **kwargs)

        response = HttpResponse(status=401)
        response['WWW-Authenticate'] = 'Basic realm="Animal staff API"'
        return response
    return _wrapped_view