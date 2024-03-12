# Generated by Django 3.2.15 on 2024-03-05 11:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0044_alter_order_details_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_details',
            name='cost',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Стоимость'),
        ),
    ]