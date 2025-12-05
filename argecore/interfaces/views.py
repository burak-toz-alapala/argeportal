from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.shortcuts import redirect


def group_required(groups):
    """
    groups: Tek grup adı (string) veya birden fazla grup ismi (list/tuple)
    """
    if isinstance(groups, str):
        groups = [groups]  # Tek string verilirse listeye çevir

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('/login')

            # Kullanıcının belirtilen gruplardan en az birinde olması gerekiyor
            if not request.user.groups.filter(name__in=groups).exists():
                return redirect('/no-permissions')

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# Create your views here.
@group_required(['silo', 'engineer'])
def home_page(request):
    return render(request, 'silo_calculate.html')

@login_required(login_url='/login')
def tmp_page(request):
    return render(request, 'tmp.html')

@login_required(login_url='/login')
def no_permissions_page(request):
    return render(request, 'no-permissions.html')

@login_required(login_url='/login')
def profile_page(request):
    return render(request, 'profile.html')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'login.html')


