from rest_framework.serializers import ModelSerializer
from foodcartapp.models import Order, Order_details


class Order_detailsSerializer(ModelSerializer):
    class Meta:
        model = Order_details
        fields = ['quantity', 'product']


class OrderSerializer(ModelSerializer):
    products = Order_detailsSerializer(many=True,
                                       allow_empty=False,
                                       write_only=True)
    class Meta:
        model = Order
        fields = ['firstname', 'lastname','address', 'phonenumber', 'products']


class OrderFrontendSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['firstname', 'lastname','address', 'phonenumber', 'id']
