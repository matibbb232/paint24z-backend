from django.urls import path
from .views import ClientOrdersView
from .views import (
    get_about,
    get_categories,
    get_manufacturers,
    get_product,
    get_products,
    get_store,
    get_orders,
    make_order,
)

urlpatterns = [
    path("products/", get_products, name="Products"),
    path("product/<int:id>/", get_product, name="product_detail"),
    path("categories/", get_categories, name="categories"),
    path("about/", get_about, name="about"),
    path("manufacturers/", get_manufacturers, name="manufacturers"),
    path("store/", get_store, name="store"),
    path("orders/", get_orders, name="orders"),
    path('client/<int:client_id>/orders/', ClientOrdersView.as_view(), name='client-orders'),
    path('makeorder/', make_order, name='make_order')
]
