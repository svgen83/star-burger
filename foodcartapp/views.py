from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response

import json


from .models import Product, Order, Order_details


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

@api_view(['POST'])
def register_order(request):
    # TODO это лишь заглушка
    order_description = request.data
    print(order_description)


    if not 'products' in order_description:
        return Response(f'Поле Продукты не может отсутствовать. Это обязательное поле')
    if not order_description['products']:
        return Response(f'Поле Продукты не может быть пустым. Это обязательное поле')
    if not isinstance(order_description['products'], list):
        return Response(f'В поле Продукты ожидается ввод списка')

    
    order_db, created = Order.objects.get_or_create(
        firstname=order_description['firstname'],
        lastname=order_description['lastname'],
        contact_phone=order_description['phonenumber'],
        address=order_description['address']
    )
    
    all_products = Product.objects.all()
    for product in order_description['products']:
        
        Order_details.objects.get_or_create(
            order=order_db,
            product=all_products.get(id=product['product']),
            product_count=product['quantity']
            )
    return Response({})

