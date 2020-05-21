from django.shortcuts import render, redirect, get_object_or_404, Http404
from django.contrib.auth import authenticate, login, get_user_model
from django.http import JsonResponse, HttpResponse
from shop.forms import ContactForm
from django.views.generic import ListView, DetailView
from .models import Product
from carts.models import Cart


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'shop/product_list.html'
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(ProductListView, self).get_context_data(**kwargs)
    #     return context


def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, 'shop/product_list.html', context)


class ProductDetailSlugView(DetailView):
    model = Product
    template_name = 'shop/detail_list.html'

    def get_context_data(self, **kwargs):
        request = self.request
        context = super(ProductDetailSlugView, self).get_context_data()
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        instance = get_object_or_404(Product, slug=slug)
        return instance


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = 'shop/detail_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        print(context)
        return context
    # def get_object(self):
    #     request = self.request
    #     product_id = self.kwargs.get('product_id')
    #     instance = Product.objects.get_by_id(product_id)
    #     if instance is None:
    #         raise Http404("product doesn't exist")
    #     return instance


def product_detail_view(request, product_id):
    # instance =  get_object_or_404(Product, pk=product_id)
    instance = Product.objects.get_by_id(product_id)
    if instance is None:
        raise Http404("product doesn't exist")

    context = {
        'object': instance
    }
    return render(request, 'shop/detail_list.html', context)


def home_page(request):
    context = {}
    if request.user.is_authenticated:
        context["premium_content"] = "ouh u r registred"
    return render(request, "shop/index.html", context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
        if request.is_ajax():
            return JsonResponse({"message":"thank you!"})
    if contact_form.errors:
        errors=contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type='application/json')
    return render(request, 'shop/contact_page.html', {"form": contact_form})


class ProductFeaturedListView(ListView):
    template_name = 'shop/product_list.html'

    def get_queryset(self):
        request = self.request
        return Product.objects.featured()


class ProductFeaturedDetailView(DetailView):
    template_name = 'shop/featured-detail.html'
    queryset = Product.objects.featured()
