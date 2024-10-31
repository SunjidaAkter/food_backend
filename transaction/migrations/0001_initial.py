# Generated by Django 5.0.4 on 2024-10-31 11:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_accounts', '0004_useraccounts_payment_status_useraccounts_trans_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_url', models.URLField(blank=True, max_length=100, null=True)),
                ('transaction_id', models.CharField(blank=True, max_length=100, null=True)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('amount', models.IntegerField(default=0)),
                ('trans_type', models.CharField(choices=[('Deposit', 'Deposit'), ('Withdraw', 'Withdraw')], default='Deposit', max_length=15)),
                ('payment_status', models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed'), ('Cancelled', 'Cancelled')], default='Pending', max_length=10)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_accounts.useraccounts')),
            ],
        ),
    ]
