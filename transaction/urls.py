from django.urls import path
from .views import  transaction_success, transaction_fail, transaction_cancel,TransactionViewSet,AllUserTransactionListAPIView
from orders.views import download_order_pdf

urlpatterns = [
    path('account_transaction/', TransactionViewSet.as_view({'post': 'create'}), name='transaction'),
    path('success/', transaction_success, name='transaction_success'),
    path('fail/', transaction_fail, name='transaction_fail'),
    path('cancel/', transaction_cancel, name='transaction_cancel'),
    path('list/', AllUserTransactionListAPIView.as_view(), name='transaction_list'),
    path('download/order_pdf/<int:order_id>/',download_order_pdf , name='download_order_pdf'),
]