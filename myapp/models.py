from django.db import models
import uuid

def product_directory_path(instance, filename):
    filename = f'product_{uuid.uuid4()}_{filename}'
    return filename

class Product(models.Model):

    name = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    image = models.ImageField(upload_to=product_directory_path)
    price = models.IntegerField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta():
        db_table = 'product'

class Category(models.Model):
    
    category_name = models.CharField(max_length=50)
    is_active = models.BooleanField()

    class Meta():
        db_table = 'category'
