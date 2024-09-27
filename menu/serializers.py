from rest_framework import serializers
from . import models

        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'
class CuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Cuisine
        fields = '__all__'
        
        
class MenuSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=models.Category.objects.all())
    cuisine = serializers.PrimaryKeyRelatedField(many=True, queryset=models.Cuisine.objects.all())
    review_count = serializers.SerializerMethodField()
    image = serializers.URLField(required=False)
    class Meta:
        model = models.Menu
        fields = '__all__'

    def get_review_count(self, obj):
        return obj.review_set.count()  # Count the number of related reviews
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = '__all__'
