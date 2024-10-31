from django.db import models
from django.contrib.auth.models import User
# Create your models here.
ROLE = [
    ('Customer', 'Customer'),
    ('Admin', 'Admin'),

]
TYPE = [
    ('Deposit', 'Deposit'),
    ('WithDraw', 'WithDraw'),

]

class UserAccounts(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.URLField(max_length=1000, blank=True, null=True)
    mobile_no = models.CharField(max_length = 12)
    payment_status = models.CharField(choices = TYPE, max_length = 10, default = "Deposit",null=True,blank=True)
    address=models.CharField(max_length=100)
    amount=models.IntegerField(default=0)
    role = models.CharField(choices = ROLE, max_length = 10, default = "Customer")
    trans_id = models.IntegerField(null=True,blank=True)
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"