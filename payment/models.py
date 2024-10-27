# from django.db import models
# from django.conf import settings
# from user_accounts.models import UserAccounts
# from orders.models import Order
# from menu.models import Menu

# STATUS_CHOICES = [
#     ('PENDING', 'Pending'),
#     ('COMPLETED', 'Completed'),
#     ('FAILED', 'Failed'),
#     ('CANCELLED', 'Cancelled'),
# ]
# class Payment(models.Model):
#     customer = models.ForeignKey(UserAccounts, on_delete = models.CASCADE)
#     transaction_id = models.CharField(max_length=100, unique=True)
#     order = models.ForeignKey(Order, on_delete = models.CASCADE)
#     menu = models.ForeignKey(Menu, on_delete = models.CASCADE)
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
#     created_at = models.DateTimeField(auto_now_add=True)
#     payment_url = models.URLField(null=True,blank=True)
#     # success_url = models.URLField(null=True,blank=True)
#     # fail_url = models.URLField(null=True,blank=True)
#     # cancel_url = models.URLField(null=True,blank=True)

#     def __str__(self):
#         return f"{self.transaction_id} - {self.status}"