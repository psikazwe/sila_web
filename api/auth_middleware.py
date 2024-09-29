from django.http import HttpResponseForbidden

class AuthUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'admin/' in request.path and not request.user.is_superuser:
            return HttpResponseForbidden()
        return self.get_response(request)
