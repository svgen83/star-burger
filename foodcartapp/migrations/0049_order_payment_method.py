# Generated by Django 3.2.15 on 2024-03-14 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0048_auto_20240314_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('CASH', 'Наличные'), ('CARD', 'Банковская карта'), ('SBP', 'Cистема быстрых платежей')], db_index=True, default='CASH', max_length=4, verbose_name='Способ оплаты'),
        ),
    ]