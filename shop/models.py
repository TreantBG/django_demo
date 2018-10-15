from django.db import models
from django.db.models import ImageField
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

from django_demo import settings


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('name',)


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    price = models.FloatField(default=0)
    category = models.ForeignKey('Category', verbose_name='Product Category', blank=False, on_delete=models.CASCADE)
    image = ImageField(upload_to='product_images')
    thumbnail = ImageSpecField(source='image',
                               processors=[ResizeToFill(100, 50)],
                               format='JPEG',
                               options={'quality': 60})

    def __str__(self):
        return self.name


class Order(models.Model):
    order_date = models.DateTimeField('date ordered')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    delivery_detiles = models.CharField(max_length=400)
    cost = models.FloatField(default=0)
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return "User " + str(self.user) + " ordered $" + str(self.cost) + " on " + str(self.order_date)


class ProductsInCart(models.Model):
    product = models.ForeignKey('Product', blank=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def line_total(self):
        return self.product.price * self.quantity

class Cart(models.Model):
    products = models.ManyToManyField(ProductsInCart, blank=True)
