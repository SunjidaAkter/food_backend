from django.urls import path
from .views import  payment_success, payment_fail, payment_cancel,PaymentViewSet
from orders.views import download_order_pdf

urlpatterns = [
    path('order_payment/', PaymentViewSet.as_view({'post': 'create'}), name='payment'),
    path('success/', payment_success, name='payment_success'),
    path('fail/', payment_fail, name='payment_fail'),
    path('cancel/', payment_cancel, name='payment_cancel'),
    path('download/order_pdf/<int:order_id>/',download_order_pdf , name='download_order_pdf'),
]