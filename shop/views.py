from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from .forms import ContactForm, LoginForm, RegisterForm


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
