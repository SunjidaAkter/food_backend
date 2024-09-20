from rest_framework import serializers
from . import models

class SpecialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Specials
        fields = '__all__'
