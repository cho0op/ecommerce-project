$(document).ready(function () {
    var stripeFormModule = $('.stripe-module-form');
    var stripeTemplate = $.templates("#stripeTemplate");
    var stripeToken = stripeFormModule.attr("data-token");
    var stripeNextUrl = stripeFormModule.attr("data-next-url");
    var stripeBtnTitle=stripeFormModule.attr("data-btn-title");
    var stripeTemplateDataContext = {
        publishKey: stripeToken,
        nextUrl: stripeNextUrl,
        btnTitle: stripeBtnTitle,
    };
    var stripeTemplateHtml = stripeTemplate.render(stripeTemplateDataContext);
    stripeFormModule.html(stripeTemplateHtml);
    var paymentForm = $('.payment-form');
    if (paymentForm.length > 1) {
        alert("Only one payment form if allowed ");
        paymentForm.css('display', 'none')
    } else if (paymentForm.length == 1) {
        var pubKey = paymentForm.attr('data-token');
        var nextUrl = paymentForm.attr('data-next-url');
        console.log(nextUrl);
    }
    // Create a Stripe client.
    var stripe = Stripe(pubKey);

    // Create an instance of Elements.
    var elements = stripe.elements();

    // Custom styling can be passed to options when creating an Element.
    // (Note that this demo uses a wider set of styles than the guide below.)
    var style = {
        base: {
            color: '#32325d',
            fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
            fontSmoothing: 'antialiased',
            fontSize: '16px',
            '::placeholder': {
                color: '#aab7c4'
            }
        },
        invalid: {
            color: '#fa755a',
            iconColor: '#fa755a'
        }
    };

    // Create an instance of the card Element.
    var card = elements.create('card', {style: style});

    // Add an instance of the card Element into the `card-element` <div>.
    card.mount('#card-element');

    // Handle real-time validation errors from the card Element.
    card.on('change', function (event) {
        var displayError = document.getElementById('card-errors');
        if (event.error) {
            displayError.textContent = event.error.message;
        } else {
            displayError.textContent = '';
        }
    });

    // Handle form submission.
    var form = document.getElementById('payment-form');
    form.addEventListener('submit', function (event) {
        event.preventDefault();

        stripe.createToken(card).then(function (result) {
            if (result.error) {
                // Inform the user if there was an error.
                var errorElement = document.getElementById('card-errors');
                errorElement.textContent = result.error.message;
            } else {
                // Send the token to your server.
                stripeTokenHandler(nextUrl, result.token);
            }
        });
    });

    function redirectToPath(nextPath, timeOffset) {
        if (nextPath) {
            setTimeout(function () {
                window.location.href = nextPath;
            }, timeOffset)
        }
    }

    // Submit the form with the token ID.
    function stripeTokenHandler(nextUrl, token) {
        var paymentMethodEndpoint = '/billing/payment-method/create/';
        var data = {
            "token": token.id
        };
        $.ajax({
            data: data,
            url: paymentMethodEndpoint,
            method: "POST",
            success: function (data) {
                card.clear();
                if (nextUrl) {
                    $.alert({
                        title: "success!",
                        content: "card is added <i class='fa fa-spin fa-spinner'></i>Redirecting",
                        theme: "modern",
                    });
                    redirectToPath(nextUrl, 1500);
                } else {
                    $.alert({
                        title: "success!",
                        content: "card is added!",
                        theme: "modern",
                    });
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    }
});