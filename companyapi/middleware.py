# your_project/middleware.py

from django.http import HttpResponseForbidden

class SilkAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # If the user is not authenticated, or not an admin or superuser, return Forbidden response
        if request.path.startswith('/silk/') and not (request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff)):
            return HttpResponseForbidden("You are not authorized to access this page.")
        response = self.get_response(request)
        return response
