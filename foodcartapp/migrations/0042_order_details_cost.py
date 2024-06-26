# Generated by Django 3.2.15 on 2024-02-22 11:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0041_auto_20240214_1121'),
    ]

    operations = [
        migrations.AddField(
            model_name='order_details',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Стоимость'),
            preserve_default=False,
        ),
    ]
