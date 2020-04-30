from django.urls import path
from . import views

urlpatterns=[
    path('<slug:slug>/', views.ProductDetailSlugView.as_view(), name='detail'),
    path('', views.ProductListView.as_view()),
]