# Generated by Django 3.2.15 on 2024-06-18 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0056_alter_location_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='coordinates',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Широта'),
        ),
    ]
