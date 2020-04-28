from django.db import models
import os, random

def get_filename_ext(filepath):
    base_name=os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self.db)
    def featured(self):
        return self.get_queryset().featured()
    def get_by_id(self,id):
        qs = self.get_queryset().filter(id=id)
        if qs.count()==1:
            return qs.first()
        return

class ProductQuerySet(models.QuerySet):
    def featured(self):
        return self.filter(featured=True)

def upload_image_path(instance, filename):
    print(instance)
    print(filename)
    new_filename= random.randint(1, 323232)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "products/img/{final_filename}".format(new_filename=new_filename, final_filename=final_filename )

class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True)
    desctiption = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=5)
    image = models.ImageField(upload_to=upload_image_path, blank=True, null=True)
    objects = ProductManager()
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title
# Create your models here.
