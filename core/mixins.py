from django.http import HttpResponseForbidden

class HROnlyMixin:
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and hasattr(user, 'employee'):
            if user.employee.department and user.employee.department.name == "Human Resources":
                return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden("You are not authorized to access this page.")