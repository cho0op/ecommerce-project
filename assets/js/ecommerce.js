
$(document).ready(function () {
    //Contact form

    var contactForm = $(".contact-form");
    var contactFormMethod = contactForm.attr("method");
    var contactFormAction = contactForm.attr("action");

    function displaySubmitting(btn, defaultTxt, doSubmit) {
        if (doSubmit) {
            btn.addClass('disabled');
            btn.html("<i class='fa fa-spin fa-spinner'></i>Sending...")
        } else {
            btn.removeClass('disabled');
            btn.html(defaultTxt)
        }
    }

    contactForm.submit(function (event) {
        event.preventDefault();
        var contactFormSubmitBtn = contactForm.find("[type='submit']");
        var contactFormSubmitBtnText = contactFormSubmitBtn.text();
        var contactFormData = contactForm.serialize();
        var thisForm = $(this);
        displaySubmitting(contactFormSubmitBtn,"", true);
        $.ajax({
            method: contactFormMethod,
            url: contactFormAction,
            data: contactFormData,
            success: function (data) {
                thisForm[0].reset();
                $.alert({
                    title: "success!",
                    content: data.message,
                    theme: "modern",
                });
                setTimeout(function () {
                    displaySubmitting(contactFormSubmitBtn,contactFormSubmitBtnText, false)
                }, 2000)
            },
            error: function (error) {
                console.log(error);
                var jsonData = error.responseJSON;
                var msg = "";
                $.each(jsonData, function (key, value) {
                    msg += key + ":" + value[0].message + "<br>"
                });
                $.alert({
                    title: "errorrrrrrrrrr.//2.sa.d/......",
                    content: msg,
                    theme: "modern",
                });
                setTimeout(function () {
                    displaySubmitting(contactFormSubmitBtn,contactFormSubmitBtnText, false)
                }, 1000)
            }
        })
    });
    //Auto Search
    var searchForm = $('.search-form');
    var searchInput = searchForm.find("[name='q']");
    var searchBtn = searchForm.find("[type='submit']");
    var typingInterval = 1000;

    function doSearch() {
        searchBtn.addClass("disabled");
        searchBtn.html("<i class='fa fa-spin fa-spinner'></i> Searching...");
    }

    function perfomSearch() {
        console.log("perfom");
        var query = searchInput.val();
        setTimeout(function () {
            window.location = "/search/?q=" + query;
        }, 1000)
    }

    searchInput.keyup(function (event) {
        typingTimer = setTimeout(perfomSearch, typingInterval);
    });
    searchInput.keydown(function () {
        searchBtn.addClass("disabled");
        searchBtn.html("<i class='fa fa-spin fa-spinner'></i> Searching...");
        clearTimeout(typingTimer);
    });
    //cart and products
    var productForm = $(".form-product-ajax");
    productForm.submit(function (event) {
        event.preventDefault();
        var thisForm = $(this);
        //var actionEndpoint=thisForm.attr("action");
        var actionEndpoint = thisForm.attr('data-endpoint');
        var httpMethod = thisForm.attr("method");
        var formData = thisForm.serialize();
        $.ajax({
            url: actionEndpoint,
            method: httpMethod,
            data: formData,
            success: function (data) {
                var submitSpan = thisForm.find('.submit-span');
                if (data.added) {
                    submitSpan.html('<button type="submit" class="btn btn-danger">Remove</button>')
                } else {
                    submitSpan.html('<button type="submit" class="btn btn-success">Add to cart</button>')
                }
                var navbarCount = $('.navbar-cart-count');
                navbarCount.text(data.cartItemCount);
                var currentPath = window.location.href;
                if (window.location.href.indexOf('cart') != -1) {
                    refreshCart();
                }
            },
            error: function (errorData) {
                $.alert({
                    title: "errorrrrrrrrrr.//2.sa.d/......",
                    content: "something went wronnngngngn",
                    theme: "modern",
                })
            }
        });
    });

    function refreshCart() {
        console.log('updating');

        var cartTable = $('.cart-table');
        var cartBody = cartTable.find('.cart-body');
        var productRows = cartBody.find(".cart-product");
        var currentUrl = location.href;
        var refreshCartUrl = '/api/cart/';
        var refreshCartMethod = "GET";
        var data = {};
        $.ajax({
            url: refreshCartUrl,
            method: refreshCartMethod,
            data: data,
            success: function (data) {
                var hiddenRemoveForm = $('.cart-item-remove-form');
                if (data.products.length > 0) {
                    console.log(">0");
                    productRows.html("");
                    $.each(data.products, function (index, value) {
                        var newHiddenRemoveForm = hiddenRemoveForm.clone();
                        newHiddenRemoveForm.css("display", 'block');
                        newHiddenRemoveForm.find('.cart-item-id').val(value.id);
                        cartBody.prepend("<tr><th scope=\"row\">" + (index + 1) + "</th><td><a href='" + value.url + "'>" + value.title + "</a>" + newHiddenRemoveForm.html() + "</td><td>" + value.price + "</td></tr>");
                    });
                    $(".cart-total").text(data.total);
                } else {
                    window.location.href = currentUrl
                }
            },
            error: function (data) {
                $.alert({
                    title: "errorrrrrrrrrr.//2.sa.d/......",
                    content: "something went wronnngngngn",
                    theme: "modern",
                })
            }
        })
    }
})
