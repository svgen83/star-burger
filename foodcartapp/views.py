from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.serializers import ValidationError, Serializer, CharField

from phonenumber_field.serializerfields import PhoneNumberField

import json


from .models import Product, Order, Order_details


class OrderSerializer(Serializer):
    firstname = CharField()
    lastname = CharField()
    address = CharField()
    phonenumber = PhoneNumberField()



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


def validate(request_data):
    errors = []
    if (not 'products' in request_data
        or not 'firstname' in request_data
        or not 'lastname' in request_data
        or not 'phonenumber' in request_data
        or not 'address' in request_data):
        errors.append('Отсутствует одно из полей заказа')
    if (not request_data['products']
        or not request_data['firstname']
        or not request_data['lastname']
        or not request_data['phonenumber']
        or not request_data['address']):
        errors.append('Поле заказа не может быть пустым. Введите данные')
    if not isinstance(request_data['products'], list):
        errors.append('В поле Продукты ожидается ввод списка')
    if not isinstance(request_data['firstname'], str):
        errors.append('В поле Имя ожидается ввод строки')
    if not PhoneNumber.from_string(request_data['phonenumber']).is_valid():
        errors.append('Введите корректные данные в поле Телефон')
    if errors:
        raise ValidationError(errors)


def validate_s(request_data):
    serializer = OrderSerializer(data = request_data)
    serializer.is_valid(raise_exception=True)


@api_view(['POST'])
def register_order(request):
    # TODO это лишь заглушка
    order_description = request.data
    print(order_description)
    #validate(order_description)
    validate_s(order_description)


##    if (not 'products' in order_description or not 'firstname' in order_description
##    or not 'lastname' in order_description or not 'phonenumber' in order_description
##    or not 'address' in order_description):
##        raise ValidationError(['Отсутствует одно из полей заказа. Это обязательное поле'])
##    if (not order_description['products']
##        or not order_description['firstname']
##        or not order_description['lastname']
##        or not order_description['phonenumber']
##        or not order_description['address']):
##        raise ValidationError(['Поле заказа не может быть пустым. Введите данные'])
##    if not isinstance(order_description['products'], list):
##        raise ValidationError(['В поле Продукты ожидается ввод списка'])
##    if not isinstance(order_description['firstname'], str):
##        raise ValidationError(['В поле Имя ожидается ввод строки'])
##    if not PhoneNumber.from_string(order_description['phonenumber']).is_valid():
##        raise ValidationError(['Введите корректные данные в поле Телефон'])

    
    order_db, created = Order.objects.get_or_create(
        firstname=order_description['firstname'],
        lastname=order_description['lastname'],
        contact_phone=order_description['phonenumber'],
        address=order_description['address']
    )
    
##    all_products = Product.objects.all()
##    for product in order_description['products']:
##        if not product['product'] in all_products:
##            raise ValidationError(['Указанного товара нет'])
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

