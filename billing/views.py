from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from billing.models import BillingProfile, Card
import stripe

STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY")
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY")
stripe.api_key = STRIPE_SECRET_KEY


def payment_method_view(request):
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_ger(request)
    if not billing_profile:
        return redirect("carts:home")
    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    return render(request, 'billing/payment-method.html', {"publish_key": STRIPE_PUB_KEY, "next_url": next_url})


def payment_method_create_view(request):
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_ger(request)
    if not billing_profile:
        return HttpResponse({'message': "cant find user"}, status_code=401)
    token = request.POST.get('token')
    if token is not None:
        new_cart_obj = Card.objects.add_new(billing_profile, token)
    if request.method == "POST" and request.is_ajax():
        return JsonResponse({"message": "done"})
    return HttpResponse("error", status=401)
# Create your views here.
