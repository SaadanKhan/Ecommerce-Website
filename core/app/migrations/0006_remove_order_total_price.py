# Generated by Django 4.1.3 on 2022-12-02 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_order_total_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total_price',
        ),
    ]