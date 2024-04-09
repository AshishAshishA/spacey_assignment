from rest_framework.authentication import TokenAuthentication

class CustomTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        # Allow access without token for the Swagger UI
        if request.path.startswith('/swagger/') or request.path.startswith('/redoc/'):
            return None
        return super().authenticate(request)
