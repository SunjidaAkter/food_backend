from django.db import models
from django.contrib.auth.models import User
# Create your models here.
ROLE = [
    ('Customer', 'Customer'),
    ('Admin', 'Admin'),

]

class UserAccounts(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.ImageField(upload_to='user_accounts/images/')
    mobile_no = models.CharField(max_length = 12)
    address=models.CharField(max_length=100)
    amount=models.IntegerField(default=0)
    role = models.CharField(choices = ROLE, max_length = 10, default = "Customer")
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"