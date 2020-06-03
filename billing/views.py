from django.shortcuts import render
import stripe

stripe.api_key = "sk_test_uAMQwOWADa01RqYBsCucGkhF00rOxC8nDa"
STRIPE_PUB_KEY = "pk_test_1qDV1Bm7yRQqOGJhUwWdVN9F001dQvT4Ir"


def payment_method_post(request):
    if request.method == "POST":
        print(request.POST)
    return render(request, 'billing/payment-method.html', {"publish_key": STRIPE_PUB_KEY})

# Create your views here.
