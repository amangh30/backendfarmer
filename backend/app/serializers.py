from rest_framework import serializers
from .models import User, Product




class UserInputSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    state = serializers.CharField()
    seller = serializers.BooleanField(required=False)

    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists!")
        return value

    def validate_password(self,value):
        if len(value) < 6:
            raise serializers.ValidationError("Password must be minimum 6 Characters!")
        return value
        
class UserOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
   class Meta:
        model = Product
        fields = '__all__'



class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate_password(self,value):
        if len(value) < 6:
            raise serializers.ValidationError("Password must be minimum 6 Characters!")
        return value