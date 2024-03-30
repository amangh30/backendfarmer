from django.db import models
import uuid
from django.contrib.auth.hashers import make_password,check_password

# Create your models here.
class User(models.Model):
    # uid = models.CharField(max_length=100, default=uuid.uuid4(), primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    password = models.CharField(max_length=150, null=False, blank=False)
    state = models.CharField(max_length=50, null=False, blank=False)
    seller = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.email = self.email.upper()
        self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)

    def is_correct_password(self,password:str):
        if check_password(password,self.password):
            return True
        return False

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

class Product(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    stock = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
