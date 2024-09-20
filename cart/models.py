from django.db import models

# Create your models here.
from django.db import models
from user_accounts.models import UserAccounts
from menu.models import Menu
# from django.contrib.auth.models import User
# Create your models here.



class Cart(models.Model):
    customer = models.ForeignKey(UserAccounts, on_delete = models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete = models.CASCADE)
    quantity = models.IntegerField()
    created_on = models.DateField(auto_now_add=True)
    cost=models.IntegerField(default=0)
    
    def __str__(self):
        return f"User : {self.customer.user.first_name} , Menu Item : {self.menu.title}"
    