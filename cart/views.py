from rest_framework import viewsets
from . import models
from . import serializers
from rest_framework.exceptions import ValidationError

class CartViewSet(viewsets.ModelViewSet):
    queryset = models.Cart.objects.all()
    serializer_class = serializers.CartSerializer

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
