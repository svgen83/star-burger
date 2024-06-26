from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone

from django.db.models import F

from django.conf import settings
from restaurateur.geotools import fetch_coordinates


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )
    longitude = models.CharField(
        'Долгота', max_length=20,
        blank=True, null=True
        )
    latitude = models.CharField(
        'Широта', max_length=20,
        blank=True, null=True
        )

    def save(self, *args, **kwargs):
        self.latitude, self.longitude = fetch_coordinates(
            settings.YANDEX_API_KEY,
            self.address)
        super(Restaurant, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class Order(models.Model):
    ORDER_STATUS = (
        ('N', 'New order is accepted'),
        ('P', 'Order is being prepared'),
        ('D', 'Delivery'),
        ('C', 'Completed'),
    )
    PAYMENT = (
        ('CASH', 'Наличные'),
        ('CARD', 'Банковская карта'),
        ('SBP', 'Cистема быстрых платежей'),
    )

    firstname = models.CharField(
        'имя заказчика',
        max_length=50
    )
    lastname = models.CharField(
        'фамилия заказчика',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    phonenumber = PhoneNumberField(
        'телефон заказчика',
        max_length=50,
        blank=True,
    )
    status = models.CharField(
        'Статус заказа',
        max_length=1,
        choices=ORDER_STATUS,
        default='N',
        db_index=True
    )
    comment = models.CharField(
        'Комментарий',
        max_length=200,
        blank=True
    )
    order_time = models.DateTimeField(
        'Время создания заказ',
        null=True,
        blank=True,
        default=timezone.now,
        db_index=True
    )
    call_time = models.DateTimeField(
        'Время звонка',
        null=True,
        blank=True,
        db_index=True
    )
    delivery_time = models.DateTimeField(
        'Время доставки',
        null=True,
        blank=True,
        db_index=True
    )
    payment_method = models.CharField(
        'Способ оплаты',
        max_length=4,
        choices=PAYMENT,
        default='CASH',
        db_index=True
    )
    restaurant = models.ForeignKey(
        Restaurant,
        verbose_name='Ресторан, где готовят заказ',
        related_name='orders_prepared',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'заказчик'
        verbose_name_plural = 'заказчики'

    def __str__(self):
        return self.lastname


class OrderDetailsQuerySet(models.QuerySet):

    def get_cost(self):
        order_details = self.annotate(
            order_cost=F('product__price') * F('quantity'))
        cost = 0
        for order_detail in order_details:
            cost += order_detail.order_cost
        return cost


class OrderDetails(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name='Заказ',
        related_name='client',
        on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product,
        verbose_name='Блюдо',
        related_name='products',
        on_delete=models.CASCADE)
    quantity = models.IntegerField(
        verbose_name='Количество',
        validators=[
            MaxValueValidator(10)])
    cost = models.DecimalField(
        'Стоимость',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)])

    objects = OrderDetailsQuerySet.as_manager()

    class Meta:
        verbose_name = 'состав заказа'
        verbose_name_plural = 'состав заказов'

    def __str__(self):
        return self.order.lastname


class Location(models.Model):
    address = models.CharField(
        'Адрес',
        max_length=100,
        blank=True, null=True,
        unique=True
    )
    longitude = models.CharField(
        'Долгота',
        blank=True, null=True,
        max_length=10)
    latitude = models.CharField(
        'Широта',
        blank=True, null=True,
        max_length=10)
    last_update = models.DateField(
        'Дата последнего обновления',
        blank=True, null=True,
        auto_now=True
    )

    class Meta:
        verbose_name = 'Месторасположение'
        verbose_name_plural = 'Месторасположения'

    def __str__(self):
        return self.address
