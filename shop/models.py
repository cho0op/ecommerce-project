from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
from django.db.models import Q

import os, random
from .utils import unique_slug_generator

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

class ProductQuerySet(models.QuerySet):
    def featured(self):
        return self.filter(featured=True)

    def active(self):
        return self.filter(active=True)

    def search(self, query):
        lookups = (
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(tag__title__icontains=query)
                  )  # contain in title or in dicription
        return self.filter(lookups).distinct()  #.distict - delete duplicate products when query is in title and discription

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self.db)

    def featured(self):
        return self.get_queryset().featured()

    def active(self):
        return self.get_queryset().active()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return
    def search(self, query):
        return self.get_queryset().search(query)

def upload_image_path(instance, filename):
    print(instance)
    print(filename)
    new_filename = random.randint(1, 323232)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "products/img/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)


class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, null=True, unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=5)
    image = models.ImageField(upload_to=upload_image_path, blank=True, null=True)
    objects = ProductManager()
    featured = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)
# Create your models here.
