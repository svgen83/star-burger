import logging

from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.db import transaction

from .models import Product, Order, OrderDetails, Location
from .serializers import OrderSerializer, OrderFrontendSerializer
from restaurateur.geotools import fetch_coordinates
from django.conf import settings


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            } if product.category else None,
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)

    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


@transaction.atomic
@api_view(['POST'])
def register_order(request):
    serializer = OrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    order_db = serializer.data
    try:
        location = Location.objects.get_or_create(
            address=order_db['address'],
        )
    except Location.DoesNotExist:
        try:
            coordinates = fetch_coordinates(
                settings.YANDEX_API_KEY,
                order_db['address']
                )
            location = Location.objects.create(
                address=order_db['address'],
                latitude=coordinates[0],
                longitude=coordinates[1]
                )
        except requests.exceptions.HTTPError as err:
            logging.error(err)
            pass
    serializer_response = OrderFrontendSerializer(data=order_db)
    serializer_response.is_valid(raise_exception=True)
    return Response(order_db)
