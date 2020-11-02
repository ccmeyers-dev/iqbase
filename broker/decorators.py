from django.shortcuts import redirect

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_admin:
            return redirect('dashboard')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def verified_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_verified:
            return redirect('action_block')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def setup_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_setup:
            return redirect('profile')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func