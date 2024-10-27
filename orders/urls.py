from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter() 
router.register('', views.OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('download-order-pdf/<int:order_id>/', views.download_order_pdf, name='download_order_pdf'),
]

