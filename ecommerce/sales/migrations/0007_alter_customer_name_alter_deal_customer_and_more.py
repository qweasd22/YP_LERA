# Generated by Django 5.2 on 2025-05-05 12:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0006_remove_deal_discount_remove_deal_total_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Покупатель'),
        ),
        migrations.AlterField(
            model_name='deal',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales.customer', verbose_name='Клиент'),
        ),
        migrations.AlterField(
            model_name='deal',
            name='date',
            field=models.DateField(auto_now_add=True, verbose_name='Дата'),
        ),
    ]
