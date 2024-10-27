
import uuid
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
from orders.models import Order
from menu.models import Menu
from . import models



global_data = {}
arr = []
arr1=[]
def generate_transaction_id():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    unique_id = uuid.uuid4().hex[:6].upper()
    return f'TXN-{timestamp}-{unique_id}'


class PaymentSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    menu_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    mobile = serializers.CharField(max_length=500)
    address = serializers.CharField(max_length=500)
    email = serializers.EmailField(max_length=500)

    def validate(self, data):
        order_id = data.get('order_id')
        menu_id = data.get('menu_id')
        user_id = data.get('user_id')
        mobile = data.get('mobile')
        address = data.get('address')
        email = data.get('email')

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            raise serializers.ValidationError({'error': _('Order does not exist')})

        try:
            user_accounts = UserAccounts.objects.get(user_id=user_id)  
        except UserAccounts.DoesNotExist:
            raise serializers.ValidationError({'error': _('User account does not exist')})
        
        try:
            menu = Menu.objects.get(menu_id=menu_id)
        except Menu.DoesNotExist:
            raise serializers.ValidationError({'error': _('Menu item does not exist')})

        
        data['order'] = order
        data['user_accounts'] = user_accounts
        data['menu'] = menu
        data['mobile'] = mobile
        data['address'] = address
        data['email'] = email
        return data

    def create(self, validated_data):
        try:
            user_id = validated_data.pop('user_id')
            order_id = validated_data.pop('order_id')
            menu_id = validated_data.pop('menu_id')
            mobile = validated_data['mobile']
            address = validated_data['address']
            email = validated_data['email']

            with transaction.atomic():
                transaction_id = generate_transaction_id()
                settings = {
                    'store_id': 'sunji671d9d2a3a509',
                    'store_pass': 'sunji671d9d2a3a509@ssl',
                    'issandbox': True
                }

                sslcz = SSLCOMMERZ(settings)
                order = validated_data['order']
                menu = validated_data['menu']
                user_accounts = validated_data['user_accounts']
                post_body = {
                    'total_amount': order.cost,
                    'currency': "BDT",
                    'tran_id': transaction_id,
                    'success_url': 'https://hotel-booking-website-backend.vercel.app/payment/success/', # slashe
                    'fail_url': 'https://hotel-booking-website-backend.vercel.app/payment/fail/',
                    'cancel_url': 'https://hotel-booking-website-backend.vercel.app/payment/cancel/',
                    'emi_option': 0,
                    'cus_name': user_accounts.user.first_name,
                    'cus_email': email,
                    'cus_phone': mobile,
                    'cus_add1': address,
                    'cus_city': "Dhaka",
                    'cus_country': "Bangladesh",
                    'shipping_method': "YES",
                    'num_of_item': order.quantity,
                    'product_name': menu.title,
                    'product_category': menu.category,
                }

                response = sslcz.createSession(post_body)

                if response.get('status') == 'SUCCESS':
                    gateway_url = response['GatewayPageURL']

                    # Update the Order fields
                    order.transaction_id = transaction_id
                    order.payment_url = gateway_url
                    order.save()

                    # Create initial payment record with 'PENDING' status
                    payment = models.Payment.objects.create(
                        order=order,
                        menu=menu,
                        customer=user_accounts,
                        payment_url=gateway_url,
                        transaction_id=transaction_id,
                        status='PENDING'
                    )

                    # Store global data
                    payment_id = payment.id
                    global_data[transaction_id] = user_accounts
                    arr.append(order_id)
                    arr1.append(payment_id)
                    return {
                        'order_id': order.id,
                        'payment_url': gateway_url,
                        'transaction_id': transaction_id
                    }
                else:

                    # If payment failed, save a failed payment record
                    models.Payment.objects.create(
                        order=order,
                        menu=menu,
                        customer=user_accounts,
                        transaction_id=transaction_id,
                        payment_url=gateway_url,
                        status='FAILED'
                    )
                    raise serializers.ValidationError({'error': _('Failed to create payment session')})

        except Exception as e:
            raise serializers.ValidationError({'error': _('Failed to create booking.')})

class PaymentViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = PaymentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            payment_data = serializer.save()
            return Response(payment_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        transaction_id = request.POST.get('tran_id')
        if arr and arr1:
            arr_id = arr.pop(0)
            pay_id = arr1.pop(0)
        else:
            arr_id = None
            pay_id=None
        
        if arr_id is None and pay_id is None:
            return render(request, 'payment_fail.html')

        try:
            payment=models.Payment.objects.get(id=pay_id)
            order = Order.objects.get(id=arr_id)
            menu=order.menu
            user_accounts = global_data.get(transaction_id)
            if not user_accounts:
                raise ValidationError({"error":"User Account not found"})

            payment.status = 'COMPLETED'
            payment.save(update_fields=['status'])

            order.is_paid=True
            order.save(update_fields=['is_paid'])

            email_subject = _("Payment Confirmation")
            email_body = render_to_string('payment_confirm_email.html', {
                'order': order,
                'payment': payment,
                'user': user_accounts,
                'total_cost': order.cost,
                'pdf_link': request.build_absolute_uri(reverse('download_order_pdf', args=[order.id]))
            })
            email = EmailMultiAlternatives(email_subject, '', to=[user_accounts.user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()

            context = {
                'menu': menu,
                'order': order,
                'user': user_accounts,
                'pdf_link': request.build_absolute_uri(reverse('download_order_pdf', args=[order.id])),
            }

            return render(request, 'payment_success.html', context)

        except models.Payment.DoesNotExist:
            return render(request, 'payment_fail.html')
        except Order.DoesNotExist:
            return render(request, 'payment_fail.html')
        except Menu.DoesNotExist:
            return render(request, 'payment_fail.html')

    return HttpResponse("Payment success page. This page should be accessed via POST request from the payment gateway.")
@csrf_exempt
def payment_fail(request):
    return render(request, 'payment_fail.html')
@csrf_exempt
def payment_cancel(request):
    return render(request, 'payment_cancel.html')