from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.shortcuts import redirect

def group_required(group_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('/login')
            if not request.user.groups.filter(name=group_name).exists():
                return redirect('/no-permissions')  # yetkisiz
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# Create your views here.
@group_required('worker')
def home_page(request):
    return render(request, 'silo_calculate.html')

@login_required(login_url='/login')
def tmp_page(request):
    return render(request, 'tmp.html')

@login_required(login_url='/login')
def no_permissions_page(request):
    return render(request, 'no-permissions.html')

def login_page(request):
    return render(request, 'login.html')
