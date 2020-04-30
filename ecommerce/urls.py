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


urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('shop.urls')),
    # path('',views.home_page, name="home_page"),
    # path('contact/', views.contact_page),
    # path('login/', views.login_page, name="login_page"),
    # path('register/', views.register_page, name="register_page"),
    # path('featured/', views.ProductFeaturedListView.as_view()),
    # path('featured/<int:pk>/', views.ProductFeaturedDetailView.as_view()),
    # #products
    # path('products/', views.ProductListView.as_view()),
    # path('products/<slug:slug>/', views.ProductDetailSlugView.as_view(), name='slug_detail'),
    # path('products-fbv/', views.product_list_view),
    # path('products/<int:pk>/', views.ProductDetailView.as_view()),
    # path('products-fbv/<int:product_id>/', views.product_detail_view),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)