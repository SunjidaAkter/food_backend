# Generated by Django 5.0.4 on 2024-10-29 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_order_total_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('Paid', 'Paid'), ('Pending', 'Pending'), ('Delivering', 'Delivering'), ('Unordered', 'Unordered')], default='Unordered', max_length=10),
        ),
    ]
