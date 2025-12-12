from django.db import models
from django.utils import timezone

# Create your models here.
class product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    publish_date = models.DateField()
    image = models.ImageField(upload_to='shop/images', default="")

    def __str__(self):
        return f"{self.product_name}"# - {self.category}"
    
class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    desc = models.TextField()


    def __str__(self):
        return self.name

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000,default="")
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=500)
    email = models.EmailField()
    address = models.CharField(max_length=500)
    country = models.CharField(max_length=500,default="")
    city = models.CharField(max_length=500)
    state = models.CharField(max_length=500)
    zip_code = models.CharField(max_length=500)
    phone = models.CharField(max_length=500, default="")

    def __str__(self):
        return f"Order {self.order_id} - {self.name}"

class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"OrderUpdate {self.update_id} - {self.update_desc}"