
import os.path
import os
import shutil

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django_ckeditor_5.fields import CKEditor5Field


def products_image_path(instance, filename):
    return f'products/{instance.product_id}/{filename}'


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    categories = models.ManyToManyField(Category, related_name='products')
    description = CKEditor5Field()

    def __str__(self):
        return f'{self.id}: {self.name}'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=products_image_path)

    def __str__(self):
        return f"Image for {self.product.name}"


@receiver(post_delete, sender=Product)
def delete_photos_folder(sender, instance, **kwargs):
    product_images_dir = os.path.join('media', 'products', str(instance.id))

    if os.path.exists(product_images_dir):
        shutil.rmtree(product_images_dir)
