from django.db import models

# Create your models here.
# Create Table
class Category(models.Model):
    category_name = models.CharField(max_length=75)
    reg_date = models.DateTimeField(auto_now_add=True)

    # Output of info
    def __str__(self):
        return self.category_name


class Product(models.Model):
    product_name = models.CharField(max_length=125)
    product_count = models.IntegerField()
    product_price = models.FloatField()
    product_photo = models.ImageField(upload_to='media')
    product_des = models.TextField()
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)

    reg_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name

class Cart(models.Model):
    user_id = models.IntegerField()
    user_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user_product_quantity = models.IntegerField()
    total_for_product = models.FloatField()

    def __str__(self):
        return str(self.user_product)