from django.contrib import admin
from .models import UserTransaction
# Register your models here.
@admin.register(UserTransaction)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'transaction_id','amount')
    list_filter = ('customer', 'transaction_id')
    search_fields = ('customer', 'transaction_id')