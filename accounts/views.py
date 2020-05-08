from django.shortcuts import render, redirect
from accounts.forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, get_user_model
from django.utils.http import is_safe_url


def login_page(request):
    form = LoginForm(request.POST or None)
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        form = LoginForm()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("home")
        else:
            print("error")
    return render(request, "accounts/login.html", {"form": form})


User = get_user_model()


def register_page(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        new_user = User.objects.create_user(username, email, password)
    return render(request, "accounts/register.html", {"form": form})
# Create your views here.
