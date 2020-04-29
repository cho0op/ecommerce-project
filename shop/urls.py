from django.urls import path
from shop import views


urlpatterns = [
    # path('', views.home_page, name="home_page"),
    # path('contact/', views.contact_page),
    # path('login/', views.login_page, name="login_page"),
    # path('register/', views.register_page, name="register_page"),
    # path('featured/', views.ProductFeaturedListView.as_view()),
    # path('featured/<int:pk>/', views.ProductFeaturedDetailView.as_view()),
    # # products
    # path('products/', views.ProductListView.as_view()),

    # path('products-fbv/', views.product_list_view),

    # path('products-fbv/<int:product_id>/', views.product_detail_view),
    path('', views.ProductListView.as_view()),
    path('<slug:slug>/', views.ProductDetailSlugView.as_view()),
    path('<int:pk>/', views.ProductDetailView.as_view()),
]