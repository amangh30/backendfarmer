from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import UserInputSerializer, UserOutputSerializer, ProductSerializer, UserLoginSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.http import FileResponse
from django.views import View
from django.http import HttpResponse

class DefaultView(APIView):
    def get(self, request):
        return Response({"status": 200, "message": "Welcome to the Farmers API"})
    
    def post(self, request):
        return Response({"status": 200, "message": "Welcome to the Farmers API"})

class UserView (APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserOutputSerializer(users, many=True)
        return Response({"status": 200, "payload": serializer.data})
    
    def post(self, request):
        serializer = UserInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"status": 403, "error": serializer.errors})
        user = User(
            name = serializer.data['name'],
            email = serializer.data['email'],
            password = serializer.data['password'],
            state = serializer.data['state'],
            seller = serializer.data['seller'],
        )
        refresh = RefreshToken.for_user(user)
        user.save()
        return Response({"status": 200, "payload": serializer.data, "refresh": str(refresh), "access": str(refresh.access_token)})
    
class ProductView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductImageView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        if product.image:
            return FileResponse(product.image.open('rb'), content_type='image/jpeg')
        else:
            # Return a default image or handle the case when there's no image
            return HttpResponse(status=404)  # Or any other appropriate response      


class UserLoginView(APIView):
    def get(self, request):
        return Response({"status": 405, "message": "Method Not Allowed"})
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"status": 403, "error": serializer.errors})
        user = User.objects.get(email=serializer.data['email'])
        if not user.is_correct_password(serializer.data['password']):
            return Response({"status": 403, "error": "Invalid Password"})
        refresh = RefreshToken.for_user(user)
        return Response({"status": 200, "refresh": str(refresh), "access": str(refresh.access_token),"name":user.name})
    
class UserRegisterView(APIView):
    def get(self, request):
        return Response({"status": 405, "message": "Method Not Allowed"})
    def post(self, request):
        serializer = UserInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"status": 403, "error": serializer.errors})
        user = User(
            name = serializer.data['name'],
            email = serializer.data['email'],
            password = serializer.data['password'],
            state = serializer.data['state'],
            seller = serializer.data['seller'],
        )
        refresh = RefreshToken.for_user(user)
        user.save()
        return Response({"status": 200, "refresh": str(refresh), "access": str(refresh.access_token)})