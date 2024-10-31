# middleware.py
from django.conf import settings
from django.http import JsonResponse

class APIKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check for 'Authorization' header
        api_key = request.headers.get("Authorization")
        if api_key != f"Bearer {settings.API_KEY}":
            return JsonResponse({"error": "Unauthorized"}, status=401)
        return self.get_response(request)
