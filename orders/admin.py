from django.contrib import admin
from . import models
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'menu_item', 'order_status', 'quantity', 'created_on', 'payment_status']
    def customer_name(self,obj):
        return obj.customer.user.first_name
    
    def menu_item(self,obj):
        return obj.menu.title
    
    def save_model(self, request, obj, form, change):
        obj.save()
        if obj.order_status == "Delivering":
            email_subject = "Your order has been delivered"
            email_body = render_to_string('dealer_email.html', {'customer' : obj.customer.user, 'menu' : obj.menu})
            
            email = EmailMultiAlternatives(email_subject , '', to=[obj.customer.user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
    
admin.site.register(models.Order, OrderAdmin)