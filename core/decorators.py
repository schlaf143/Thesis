# decorators.py
from django.http import HttpResponseForbidden

def hr_only(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if hasattr(request.user, 'employee'):
            employee = request.user.employee
            if employee.department.name == "Human Resources":
                return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You are not authorized to access this page.")
    return _wrapped_view
