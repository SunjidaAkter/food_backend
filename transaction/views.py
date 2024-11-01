
import uuid
from rest_framework.viewsets import ReadOnlyModelViewSet
from datetime import datetime
from django.db import transaction
from django.shortcuts import render, reverse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from sslcommerz_lib import SSLCOMMERZ
from user_accounts.models import UserAccounts
from rest_framework import generics
from orders.models import Order
from menu.models import Menu
from .models import UserTransaction
from django.shortcuts import get_object_or_404
from .serializers import AllUserTransactionSerializer

global_data = {}
arr = []
arr1=[]
def generate_transaction_id():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    unique_id = uuid.uuid4().hex[:6].upper()
    return f'TXN-{timestamp}-{unique_id}'


class TransactionSerializer(serializers.Serializer):
    
    user_id = serializers.IntegerField()
    amount = serializers.IntegerField()
    trans_type = serializers.CharField()
    def validate(self, data):
        user_id = data.get('user_id')
        amount = data.get('amount')
        trans_type = data.get('trans_type')

        
        try:
            user_accounts = UserAccounts.objects.get(id=user_id)  
        except UserAccounts.DoesNotExist:
            raise serializers.ValidationError({'error': _('User account does not exist')})
        
        
        
        data['user_accounts'] = user_accounts
        data['amount'] = amount
        data['trans_type'] = trans_type
        return data

    def create(self, validated_data):
        try:
            user_id = validated_data.pop('user_id')
            amount = validated_data['amount']
            trans_type = validated_data['trans_type']

            print("Entered transaction block ================================================")
            
            with transaction.atomic():
                print("Inside transaction.atomic() block ======================================")
                
                transaction_id = generate_transaction_id()
                settings = {
                    'store_id': 'sunji671d9d2a3a509',
                    'store_pass': 'sunji671d9d2a3a509@ssl',
                    'issandbox': True
                }

                sslcz = SSLCOMMERZ(settings)
                user_accounts = UserAccounts.objects.get(id=user_id)

                post_body = {
                    'total_amount': amount,
                    'currency': "BDT",
                    'tran_id': transaction_id,
                    'success_url': 'http://127.0.0.1:8000/transaction/success/', 
                    'fail_url': 'http://127.0.0.1:8000/transaction/fail/',
                    'cancel_url': 'http://127.0.0.1:8000/transaction/cancel/',
                    'emi_option': 0,
                    'cus_name': user_accounts.user.first_name,
                    'cus_email': user_accounts.user.email,
                    'cus_phone': user_accounts.mobile_no,
                    'cus_add1': user_accounts.address,
                    'cus_city': "Dhaka",
                    'cus_country': "Bangladesh",
                    'shipping_method': "NO",
                    'num_of_item': 0,
                    'product_name': "Transaction",
                    'product_category': "Money",
                    'product_profile': "general"
                }

                response = sslcz.createSession(post_body)

                print("Session creation response ==========================", response)

                if response.get('status') == 'SUCCESS':
                    gateway_url = response['GatewayPageURL']
                    
                    try:
                        transactions = UserTransaction.objects.create(
                            customer=user_accounts,
                            amount=amount,
                            trans_type=trans_type,
                            payment_url=gateway_url
                        )
                        # transaction.payment_url = gateway_url
                        # transaction.save(update_fields=['payment_url'])
                        trans_id = transactions.id
                        arr.append(trans_id)
                        global_data[transaction_id] = user_accounts
                        print(gateway_url)
                        return {
                            'trans_id': transactions.id,
                            'payment_url': gateway_url,
                            'transaction_id': transaction_id
                        }
                    except Exception as e:
                        print(f"Failed to create UserTransaction: {e}")
                        raise serializers.ValidationError({'error': _('Failed to create UserTransaction')})
                else:
                    raise serializers.ValidationError({'error': _('Failed to create payment session')})

        except Exception as e:
            print(f"Exception caught: {e}")
            raise serializers.ValidationError({'error': _('Failed transaction.')})

class AllUserTransactionListAPIView(viewsets.ModelViewSet):
    # queryset = Booking.objects.all()
    queryset = UserTransaction.objects.all()
    serializer_class = AllUserTransactionSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    def get_queryset(self):
        customer_id = self.request.query_params.get('customer_id')

        # If customer_id is not provided, return the full queryset
        if customer_id is None:
            return super().get_queryset()

        # Check if customer_id is a valid integer
        if not customer_id.isdigit():
            raise ValidationError({"customer_id": "Invalid customer_id. It must be a number."})

        # Filter queryset by customer_id
        return super().get_queryset().filter(customer_id=int(customer_id))
    

class TransactionViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = TransactionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            payment_data = serializer.save()
            return Response(payment_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def transaction_success(request):
    if request.method == 'POST':
        transaction_id = request.POST.get('tran_id')
        if arr :
            arr_id = arr.pop(0)
            # pay_id = arr1.pop(0)
        else:
            arr_id = None
            # pay_id=None
        
        if arr_id is None :
            return render(request, 'trans_fail.html')

        try:
            # payment=models.Payment.objects.get(id=pay_id)
            trans = UserTransaction.objects.get(id=arr_id)
            user_accounts = global_data.get(transaction_id)
            if not user_accounts:
                raise ValidationError({"error":"User Account not found"})

            # payment.status = 'COMPLETED'
            # payment.save(update_fields=['status'])
            print(transaction_id)
            trans.transaction_id = transaction_id
            trans.payment_status="Completed"
            if trans.trans_type == "Deposit":
                trans.balance_after_trans=user_accounts.amount+trans.amount
                user_accounts.amount=user_accounts.amount+trans.amount
            if trans.trans_type == "Withdraw":
                trans.balance_after_trans=user_accounts.amount-trans.amount
                user_accounts.amount=user_accounts.amount-trans.amount
            trans.save(update_fields=['transaction_id'])
            trans.save(update_fields=['balance_after_trans'])
            trans.save(update_fields=['payment_status'])
            user_accounts.save(update_fields=['amount'])
            email_subject = _("Payment Confirmation")
            email_body = render_to_string('transaction_confirm_email.html', {
                'trans': trans,
                # 'payment': payment,
                'user': user_accounts,
                'total_cost': trans.amount,
                'pdf_link': request.build_absolute_uri(reverse('download_order_pdf', args=[trans.id]))
            })
            email = EmailMultiAlternatives(email_subject, '', to=[user_accounts.user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()

            context = {
                
                'trans': trans,
                'user': user_accounts,
                'pdf_link': request.build_absolute_uri(reverse('download_order_pdf', args=[trans.id])),
            }

            return render(request, 'trans_success.html', context)

        # except models.Payment.DoesNotExist:
        #     return render(request, 'payment_fail.html')
        
        except Exception as e:
            print(f"Unexpected error: {e}=======================================================================================================================================")
            return render(request, 'trans_fail.html')
        

    return HttpResponse("Payment success page. This page should be accessed via POST request from the payment gateway.")
@csrf_exempt
def transaction_fail(request):
    return render(request, 'trans_fail.html')
@csrf_exempt
def transaction_cancel(request):
    return render(request, 'trans_cancel.html')