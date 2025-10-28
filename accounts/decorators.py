from functools import wraps
from django.http import HttpResponseForbidden


def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(request.get_full_path())
            if user.is_superuser:
                return view_func(request, *args, **kwargs)
            if hasattr(user, 'role') and user.role in roles:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden('Insufficient permissions')
        return _wrapped
    return decorator

admin_required = role_required('ADMIN')
doctor_required = role_required('DOCTOR')
patient_required = role_required('PATIENT')


