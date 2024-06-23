# urls.py
from django.urls import path
from .views import create_payment, ipn

urlpatterns = [
    path('create-payment/', create_payment, name='create_payment'),
    path('ipn/', ipn, name='ipn'),
]