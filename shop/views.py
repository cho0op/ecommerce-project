from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from .forms import ContactForm, LoginForm, RegisterForm
from django.views.generic.list import ListView
from .models import Product

class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'shop/product_list.html'
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(ProductListView, self).get_context_data(**kwargs)
    #     return context

def product_list_view(request):
    queryset = Product.objects.all()
    context={
        'object_list':queryset
    }
    return render(request, 'shop/product_list.html', context)

class ProductDetailView(ListView):
    queryset = Product.objects.all()
    template_name = 'shop/detail_list.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductDetailView, self).get_context_data( **kwargs)
        print(context)
        return context

def product_detail_view(request,product_id):
    instance =  get_object_or_404(Product, pk=product_id)
    context={
        'object' : instance
    }
    return render(request, 'shop/detail_list.html', context)

def home_page(request):
    context={}
    if request.user.is_authenticated:
        context["premium_content"]="ouh u r registred"
    return render(request, "shop/index.html", context)

def contact_page(request):
    contact_form=ContactForm(request.POST or None)
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    return render(request, 'shop/contact_page.html', {"form":contact_form})

def login_page(request):
    form=LoginForm(request.POST or None)
    if form.is_valid():
        username=form.cleaned_data.get('username')
        password=form.cleaned_data.get('password')
        form=LoginForm()
        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home_page")
        else:
            print("error")
    return render(request, "shop/auth/login.html", {"form":form})

User=get_user_model()
def register_page(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email=form.cleaned_data.get('email')
        new_user=User.objects.create_user(username, email, password)
    return render(request, "shop/auth/register.html", {"form":form})
