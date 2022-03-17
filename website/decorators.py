from django.http import HttpResponse
from django.shortcuts import redirect

# the purpose of the decorators is to reduce redundant redirect code in our views
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        # if user is already logged in, redirect home
        if request.user.is_authenticated:
            return redirect('base')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            groups = []
            if request.user.groups.exists():
                for group in request.user.groups.all():
                    # print(group.name)
                    groups.append(group.name)
            # print(allowed_roles)
            check_true = any(group_names in groups for group_names in allowed_roles)
            if check_true:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized to view this page")
        return wrapper_func
    return decorator
