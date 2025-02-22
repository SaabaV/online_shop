# Generated by Django 5.0.6 on 2024-07-23 18:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=550)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(blank=True, null=True, upload_to='media/')),
                ('discount_percentage', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('discounted_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store_app.category')),
            ],
        ),
    ]
