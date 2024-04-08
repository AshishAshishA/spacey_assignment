from rest_framework import serializers
from .models import Product, Customer, Bill, BillItem
from decimal import Decimal

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'email']

'''

class CustomerIDSerializer(serializers.Serializer):
    id = serializers.IntegerField()

class BillItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(min_value=1)  # Ensure positive quantity

    class Meta:
        model = BillItem
        fields = ['product_id', 'quantity']

class BillSerializer(serializers.ModelSerializer):
    customer = CustomerIDSerializer(source='customer.id', read_only=True)
    products = BillItemSerializer(many=True)
    # print(f"product name - {products.name}")
    class Meta:
        model = Bill
        fields = ['id', 'customer', 'products', 'total_amount', 'payment_method', 'created_at']
        read_only_fields = ['created_at', 'customer']  # Mark customer read-only (if handled elsewhere)

    def create(self, validated_data):
        print("create bill")
        products_data = validated_data.pop('products')
        

        # Validate product data (assuming products_data is a list of dictionaries)
        for product_data in products_data:
            serializer = BillItemSerializer(data=product_data['product_id'])
            serializer.is_valid(raise_exception=True)  # Raise exception for invalid product data

        bill_items = []
        total_amount = Decimal(0)

        for product_data in products_data:
            product_id = product_data['product_id']
            quantity = product_data['quantity']
            total_amount += Product.objects.get(id=product_id).price * quantity
            bill_items.append(BillItem(product_id=product_id, quantity=quantity))

        validated_data['total_amount'] = total_amount
        bill = Bill.objects.create(**validated_data)
        BillItem.objects.bulk_create(bill_items)
        return bill
'''