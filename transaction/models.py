from django.db import models

# Create your models here.
from django.db import models
from user_accounts.models import UserAccounts
# from django.contrib.auth.models import User
# Create your models here.

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Completed', 'Completed'),
    ('Failed', 'Failed'),
    ('Cancelled', 'Cancelled'),
]
TYPE = [
    ('Deposit', 'Deposit'),
    ('Withdraw', 'Withdraw'),
]
class UserTransaction(models.Model):
    customer = models.ForeignKey(UserAccounts, on_delete = models.CASCADE)
    payment_url= models.URLField(max_length=100, blank=True, null=True)
    transaction_id= models.CharField(max_length=100, blank=True, null=True)
    balance_after_trans= models.IntegerField(default=0)
    created_on = models.DateField(auto_now_add=True)
    amount=models.IntegerField(default=0)
    trans_type=models.CharField(choices= TYPE, max_length=15, default="Deposit")
    payment_status = models.CharField(choices = STATUS_CHOICES, max_length = 10, default = "Pending")

    def __str__(self):
        return f"User : {self.customer.user.first_name} , Amount : {self.amount}"
    