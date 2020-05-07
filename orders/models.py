from django.db import models

from carts.models import Cart

class Order(models.Model):
    order_id=models.CharField(max_length=120)
    #billing_profile
    #shipping_address
    #billing_address
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, default='created')
