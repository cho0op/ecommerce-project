"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from shop import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from accounts.views import register_page, login_page, guest_register_view
from django.contrib.auth.views import LogoutView
from addresses.views import checkout_address_create_view, checkout_address_reuse_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('shop.urls', namespace='products')),
    path('search/', include('search.urls', namespace='search')),
    path('cart/', include('carts.urls', namespace='carts')),
    path('', views.home_page, name="home"),
    path('checkout/address/create/', checkout_address_create_view, name='checkout_address_create'),
    path('checkout/address/reuse/', checkout_address_reuse_view, name='checkout_address_reuse'),
    path('contact/', views.contact_page, name="contacts"),
    path('login/', login_page, name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', register_page, name="register"),
    path('register/guest', guest_register_view, name="guest_register"),
    path('bootstrap/', TemplateView.as_view(template_name='bootstrap/bootstrap.html')),

    # path('featured/', views.ProductFeaturedListView.as_view()),
    # path('featured/<int:pk>/', views.ProductFeaturedDetailView.as_view()),
    # #products
    # path('products/', views.ProductListView.as_view()),
    # path('products/<slug:slug>/', views.ProductDetailSlugView.as_view(), name='slug_detail'),
    # path('products-fbv/', views.product_list_view),
    # path('products/<int:pk>/', views.ProductDetailView.as_view()),
    # path('products-fbv/<int:product_id>/', views.product_detail_view),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
