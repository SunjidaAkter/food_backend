# Generated by Django 5.0.4 on 2024-08-19 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0006_menu_reviews_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='discount',
            field=models.IntegerField(default=24),
        ),
    ]