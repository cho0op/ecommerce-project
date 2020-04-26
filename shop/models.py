from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=120)
    desctiption = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=5)
    def __str__(self):
        return self.title
# Create your models here.
