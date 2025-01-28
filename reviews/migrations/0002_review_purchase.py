# Generated by Django 5.1.5 on 2025-01-27 22:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
        ('user_cart', '0012_remove_orderitem_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='purchase',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='user_cart.purchase'),
        ),
    ]
