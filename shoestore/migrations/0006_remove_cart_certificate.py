# Generated by Django 3.1.4 on 2021-02-05 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shoestore', '0005_cart_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='certificate',
        ),
    ]
