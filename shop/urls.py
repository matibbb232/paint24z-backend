from django.urls import path
from .views import (
    get_products,
    get_product,
    get_about,
    get_cart,
    get_categories,
    get_test,
    get_manufacturers,
)

urlpatterns = [
    path("products/", get_products, name="Products"),
    path("product/<int:id>/", get_product, name="product_detail"),
    path("categories/", get_categories, name="categories"),
    path("about/", get_about, name="about"),
    path("cart/<int:id>/", get_cart, name="cart"),
    path("manufacturers/", get_manufacturers, name="manufacturers"),
]
