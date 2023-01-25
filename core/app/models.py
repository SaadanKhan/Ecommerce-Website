from django.db import models
from django.conf import Settings
from django.db import models
from django.contrib.auth.models import User
import datetime


class Category(models.Model):
       name = models.CharField(max_length = 300)

       def __str__(self):
              return self.name

       @staticmethod
       def get_all_category():
              return Category.objects.all()

class Product(models.Model):
       name = models.CharField(max_length = 200)
       price = models.IntegerField()
       image = models.ImageField(upload_to = 'product/images')
       description = models.CharField(max_length = 500 , blank = True)
       category = models.ForeignKey(Category, on_delete = models.CASCADE, default = 1)

       @staticmethod
       def get_products_by_id(ids):
              return Product.objects.filter(id__in = ids)


       def __str__(self):
              return self.name

       @staticmethod
       def get_all_products_static():
              return Product.objects.all()


       @staticmethod
       def get_all_products_category(category_id):
              return Product.objects.filter(category = category_id)

       
class Customer(models.Model):
       first_name = models.CharField(max_length=50)
       last_name = models.CharField(max_length=50)
       phone = models.CharField(max_length=20)
       email = models.EmailField()
       password = models.CharField(max_length=500)

       @staticmethod
       def get_email(email):
              try:
                     # Filter method will always returns a list, but we just want single entry
                     # therefore we have used get()
                     # return Customer.objects.filter(email=email)
                     return Customer.objects.get(email=email)
              except:
                     return False

       def __str__(self):
              return f"{self.first_name}    {self.last_name}"
       
       def isExist(self):
              if Customer.objects.filter(email=self.email):
                     return True
              else:
                     return False
                     
class Order(models.Model):
       product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
       customer = models.ForeignKey(Customer,on_delete=models.CASCADE, null=True)
       quantity = models.IntegerField(default=1)
       price = models.IntegerField()
       date = models.DateField(default=datetime.datetime.today)
