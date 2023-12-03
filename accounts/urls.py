from . import views
from django.urls import path


urlpatterns = [
    path('register', views.register_user_view, name='register_user'),
    path('verify-user', views.verify_user_view, name='verify_user'),
    path('login', views.login_user_view, name='login_user'),
    path('users', views.get_users_view, name='get_all_users'),
]