from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RideViewSet, UserViewSet


router = DefaultRouter()
router.register(r'rides', RideViewSet, basename='ride')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]

