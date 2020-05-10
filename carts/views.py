from distutils.log import Log
from billing.models import BillingProfile
from django.shortcuts import render, redirect
from .models import Cart
from shop.models import Product
from orders.models import Order
from accounts.forms import LoginForm, GuestForm
from accounts.models import GuestEmail


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, 'carts/home.html', {'cart': cart_obj})


def cart_update(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print('product doesn\'t exist')
            return redirect('carts:home')
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
        else:
            cart_obj.products.add(product_obj)
        request.session['cart_items'] = cart_obj.products.count()
    return redirect('carts:home')


def checkout_home(request):
    cart_obj, new_cart_obj = Cart.objects.new_or_get(request)
    order_obj = None
    if new_cart_obj or cart_obj.products.count() == 0:
        return redirect('carts:home')
    login_form = LoginForm()
    guest_form = GuestForm()
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_ger(request)
    if billing_profile is not None:
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile=billing_profile, cart_obj=cart_obj)
    context = {
        'object': order_obj,
        "billing_profile": billing_profile,
        'login_form': login_form,
        'guest_form': guest_form,
    }
    return render(request, 'carts/checkout.html', context)
