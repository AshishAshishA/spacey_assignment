from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CustomerViewSet, BillCreateView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth import urls

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('customers', CustomerViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Billing System API",
      default_version='v1',
      description="API for managing billing system",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@billing.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),  # Allow unauthenticated access
)


urlpatterns = [
    path('', include(router.urls)),
    path('bills/', BillCreateView.as_view()),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('accounts/', include('django.contrib.auth.urls')),  # Includes built-in authentication views
]

# path('login/', CustomAuthTokenLogin.as_view()),