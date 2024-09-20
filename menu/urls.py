from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
router = DefaultRouter()

router.register('list', views.MenuViewset)
router.register('category', views.CategoryViewset)
router.register('cuisine', views.CuisineViewset)
router.register('reviews', views.ReviewViewset)

urlpatterns = [
    path('', include(router.urls)),
]