from django.urls import path
from .views import *

urlpatterns = [
    path("", DefaultView.as_view()),
    path("user/", UserView.as_view()),
    path("product/", ProductView.as_view()),
    path("login/", UserLoginView.as_view()),
    path("register/", UserRegisterView.as_view()),
    path('products/<int:pk>/image/', ProductImageView.as_view(), name='product-image'),

]