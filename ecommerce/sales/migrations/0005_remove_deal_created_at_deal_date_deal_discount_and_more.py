# Generated by Django 5.2 on 2025-05-05 12:08

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0004_remove_product_description_alter_customer_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deal',
            name='created_at',
        ),
        migrations.AddField(
            model_name='deal',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='deal',
            name='discount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.CreateModel(
            name='DealProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('deal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deal_products', to='sales.deal')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sales.product')),
            ],
        ),
    ]
