from django.contrib.auth import views as auth_views
from django.urls import path, include


urlpatterns = [
    path('social-auth/', include('social_django.urls', namespace="social")),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    #path("login/", include('rest_social_auth.urls_session')),
]
