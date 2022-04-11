from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RemembersViewSet

app_name = 'remembers'

router = DefaultRouter()
router.register(r'remembers', RemembersViewSet, basename='remember')

urlpatterns = [
    path('', include(router.urls)),
]
