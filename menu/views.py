from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers
from rest_framework import filters, pagination
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
class CategoryViewset(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
class CuisineViewset(viewsets.ModelViewSet):
    queryset = models.Cuisine.objects.all()
    serializer_class = serializers.CuisineSerializer
    
class MenuPagination(pagination.PageNumberPagination):
    page_size = 1
    page_size_query_param = page_size
    max_page_size = 100

class MenuViewset(viewsets.ModelViewSet):
    queryset = models.Menu.objects.all()
    serializer_class = serializers.MenuSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category__name','cuisine__name','title']
    # pagination_class = MenuPagination
    search_fields = [ 'category__name', 'title','cuisine__name']
    
class ReviewsForSpecificMenu(filters.BaseFilterBackend):
    def filter_queryset(self, request, query_set, view):
        menu_id = request.query_params.get("menu_id")
        if menu_id:
            return query_set.filter(menu = menu_id)
        return query_set    
class ReviewViewset(viewsets.ModelViewSet):
    # permission_classes=[IsAuthenticatedOrReadOnly]
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer
    filter_backends = [ReviewsForSpecificMenu]

