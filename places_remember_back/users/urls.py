from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UsersViewSet

app_name = 'user_info'

router = DefaultRouter()
router.register(r'info', UsersViewSet, basename='user_info')

urlpatterns = [
    path('', include(router.urls)),
]
