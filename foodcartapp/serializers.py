from rest_framework.serializers import ModelSerializer
from foodcartapp.models import Order, OrderDetails, Product, Location
from restaurateur.geotools import fetch_coordinates
from django.conf import settings


class OrderDetailsSerializer(ModelSerializer):
    class Meta:
        model = OrderDetails
        fields = ['quantity', 'product']


class OrderSerializer(ModelSerializer):
    products = OrderDetailsSerializer(
        many=True,
        allow_empty=False,
        write_only=True)

    class Meta:
        model = Order
        fields = ['firstname', 'lastname',
                  'address', 'phonenumber',
                  'products']

    def create(self, validation_data):
        order = Order.objects.create(
            firstname=validation_data.get('firstname'),
            lastname=validation_data.get('lastname'),
            phonenumber=validation_data.get('phonenumber'),
            address=validation_data.get('address')
        )
        for product in validation_data.get('products'):
            new_detail = OrderDetails.objects.create(
            order=order,
            product=product['product'],
            quantity=product['quantity'],
            cost=Product.objects.get(name=product['product']).price
            )
            new_detail.cost_value()
        return order


class OrderFrontendSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['firstname', 'lastname', 'address', 'phonenumber', 'id']
