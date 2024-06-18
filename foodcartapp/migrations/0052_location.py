# Generated by Django 3.2.15 on 2024-06-17 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0051_auto_20240617_1100'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=100, null=True, unique=True, verbose_name='Адрес')),
                ('longitude', models.CharField(blank=True, max_length=10, null=True, verbose_name='Долгота')),
                ('latitude', models.CharField(blank=True, max_length=10, null=True, verbose_name='Широта')),
                ('last_update', models.DateField(auto_now=True, null=True, verbose_name='Дата последнего обновления')),
            ],
            options={
                'verbose_name': 'Месторасположение',
                'verbose_name_plural': 'Месторасположения',
            },
        ),
    ]
