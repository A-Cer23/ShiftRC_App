from django.urls import path, re_path
from . import views


app_name = 'users'
urlpatterns = [
    path('create/', views.CreateUser.as_view(), name='create'),
    path('login/', views.LoginUser.as_view(), name='login')
]