from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CustomerViewSet, BillCreateView, CustomAuthTokenLogin

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('customers', CustomerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('bills/', BillCreateView.as_view()),
    path('login/', CustomAuthTokenLogin.as_view())
]
