from . import views
from django.urls import path


urlpatterns = [
    path('register', views.register_user_view, name='register_user'),
    path('login', views.login_user_view, name='login_user'),
]