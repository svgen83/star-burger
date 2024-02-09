from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from phonenumber_field.phonenumber import PhoneNumber

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


    if (not 'products' in order_description or not 'firstname' in order_description
    or not 'lastname' in order_description or not 'phonenumber' in order_description
    or not 'address' in order_description):
        return Response(f'Отсутствует одно из полей заказа. Это обязательное поле',
                        status=status.HTTP_406_NOT_ACCEPTABLE)
    if (not order_description['products']
        or not order_description['firstname']
        or not order_description['lastname']
        or not order_description['phonenumber']
        or not order_description['address']):
        return Response(f'Поле заказа не может быть пустым. Введите данные',
                        status=status.HTTP_406_NOT_ACCEPTABLE)
    if not isinstance(order_description['products'], list):
        return Response(f'В поле Продукты ожидается ввод списка',
                        status=status.HTTP_406_NOT_ACCEPTABLE)
    if not isinstance(order_description['firstname'], str):
        return Response(f'В поле Имя ожидается ввод строки',
                        status=status.HTTP_406_NOT_ACCEPTABLE)
    if not PhoneNumber.from_string(order_description['phonenumber']).is_valid():
        return Response(f'Введите корректные данные в поле Телефон',
                        status=status.HTTP_406_NOT_ACCEPTABLE)

    
    order_db, created = Order.objects.get_or_create(
        firstname=order_description['firstname'],
        lastname=order_description['lastname'],
        contact_phone=order_description['phonenumber'],
        address=order_description['address']
    )
    
    all_products = Product.objects.all()
    for product in order_description['products']:
        if not product['product'] in all_products:
            return Response(f'Указанного товара нет',
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        
        Order_details.objects.get_or_create(
            order=order_db,
            product=all_products.get(id=product['product']),
            product_count=product['quantity']
            )
    return Response({})

