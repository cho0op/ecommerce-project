from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.utils.http import is_safe_url
import stripe

stripe.api_key = "sk_test_uAMQwOWADa01RqYBsCucGkhF00rOxC8nDa"
STRIPE_PUB_KEY = "pk_test_1qDV1Bm7yRQqOGJhUwWdVN9F001dQvT4Ir"


def payment_method_post(request):
    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    return render(request, 'billing/payment-method.html', {"publish_key": STRIPE_PUB_KEY, "next_url": next_url})


def payment_method_create_view(request):

    if request.method == "POST" and request.is_ajax():
        print(request.POST)
        return JsonResponse({"message": "done"})
    return HttpResponse("error", status=401)
# Create your views here.
