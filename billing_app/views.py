from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product, Customer, Bill, BillItem
from .serializers import ProductSerializer, CustomerSerializer
from decimal import Decimal

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.decorators import authentication_classes, permission_classes

# Permissions (optional)
from rest_framework.permissions import IsAuthenticated, AllowAny


# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # Permissions (optional)
    # permission_classes = [IsAuthenticated]  # Require authentication

# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # Permissions (optional)
    # permission_classes = [IsAuthenticated]  # Require authentication

# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
class BillCreateView(APIView):

    def post(self, request):
        # Extract customer data from the request data (optional)
        customer_data = request.data.get('customer')

        if customer_data:
            try:
                customer, _ = Customer.objects.get_or_create(**customer_data)
            except ValueError:  # Handle potential invalid customer data
                return Response({'error': 'Invalid customer data provided'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            customer = None  # Bill can be created without a customer

        # Extract and validate bill data
        try:
            bill_data = request.data
            products_data = bill_data.pop('products')

            # Validate required fields
            if not all([bill_data.get('payment_method'), products_data]):
                raise ValueError('Missing required fields (payment_method, products)')

            # Validate product data (assuming a list of dictionaries)
            total_amount = 0
            for product_data in products_data:
                product_id = product_data.get('id')
                quantity = product_data.get('quantity')

                if not all([product_id, quantity]):
                    raise ValueError('Invalid product data (missing id or quantity)')

                try:
                    product = Product.objects.get(pk=product_id)
                    product_data['price']=product.price
                    total_amount += product.price * quantity
                except Product.DoesNotExist:
                    raise ValueError(f'Product with ID {product_id} does not exist')

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Create the bill and bill items
        bill = Bill.objects.create(customer=customer, payment_method=bill_data['payment_method'], total_amount=total_amount)
        bill_items = [BillItem(bill=bill, product_id=product_data['id'], quantity=product_data['quantity'], price=product_data['price']) for product_data in products_data]
        BillItem.objects.bulk_create(bill_items)

        # Return the created bill data
        return Response({
            'id': bill.id,
            'customer': customer.id if customer else None,  # Include customer ID if provided
            'products': products_data,  # Consider returning only relevant product data (e.g., name, price)
            'total_amount': total_amount,
            'payment_method': bill_data['payment_method'],
            'created_at': bill.created_at
        }, status=status.HTTP_201_CREATED)


# class CustomAuthTokenLogin(ObtainAuthToken):

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'user_name': user.username,
#         })