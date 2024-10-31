from rest_framework import serializers
from django.db import transaction
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from .models import  UserTransaction
from user_accounts.models import UserAccounts
from django.utils.translation import gettext_lazy as _


class UserTransactionSerializer(serializers.Serializer):
    user_id = serializers.IntegerField() 
    amount = serializers.IntegerField()
    trans_type = serializers.CharField()
    

    def validate(self, data):
        # hotel_id = data.get('hotel_id')
        trans_type = data.get('trans_type')
        amount = data.get('amount')
        user_id = data.get('user_id') 

        
        try:
            user_account = UserAccounts.objects.get(id=user_id)
        except UserAccounts.DoesNotExist:
            raise serializers.ValidationError({'error': _('User account does not exist')})

        if trans_type=="Deposit":
            if amount<0:
                raise serializers.ValidationError({'error': _('Invalid deposit amount!')})
            
        if trans_type=="Withdraw":
            if amount>user_account.amount:
                raise serializers.ValidationError({'error': _('Insufficient amount!')})    

        
        # data['hotel'] = hotel
        data['user_account'] = user_account
        # data['total_cost'] = total_cost
        return data

    def create(self, validated_data):
        try:
            user_id = validated_data.pop('user_id')  
            user_account = validated_data['user_account']
            amount = validated_data['amount']
            trans_type = validated_data['trans_type']
            
            with transaction.atomic():
                # user_account.balance -= total_cost
                # user_account.save(update_fields=['balance'])
                if trans_type =='Deposit':
                    UserAccounts.objects.filter(id=user_account.id).update(amount=user_account.amount + amount)
                if trans_type =='Withdraw':
                    UserAccounts.objects.filter(id=user_account.id).update(amount=user_account.amount - amount)


                transaction = UserTransaction.objects.create(
                    user_id=user_id,  
                    amount=amount,
                    trans_type=trans_type
                )

                # Sending booking confirmation email
                email_subject = _("Transaction Confirmation")
                email_body = render_to_string('transaction_confirm_email.html', {
                    'user_account': user_account,
                    'amount': amount,
                    'trans_type': trans_type,
                
                    'pdf_link': self.context['request'].build_absolute_uri(reverse('download_booking_pdf', args=[transaction.id]))
                })
                email = EmailMultiAlternatives(email_subject, '', to=[user_account.user.email])
                email.attach_alternative(email_body, "text/html")
                email.send()

            return transaction
        except Exception as e:
            raise serializers.ValidationError({'error': _('Failed transaction.')})
        

class AllUserTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTransaction
        fields = '__all__'        