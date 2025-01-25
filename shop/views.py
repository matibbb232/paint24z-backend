from django.shortcuts import get_object_or_404
from rest_framework import authentication, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Addresses, Categories, Manufacturers, Orders, Products, Store, Test
from .serializers import (
    CartSerializer,
    CategoriesSerializer,
    ManufacturersSerializer,
    ProductSerializer,
    ProductsSerializer,
    StoreSerializer,
    TestSerializer,
)


@api_view(["GET"])
def get_products(request: Request) -> Response:
    """Returns list of products"""
    products = Products.objects.all()
    serializer = ProductsSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_products_by_category(request: Request, id: int) -> Response:
    """Returns products with given category id"""
    products = Products.objects.filter(category_id=id)
    serializer = ProductsSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_products_by_manufacturer(request: Request, id: int) -> Response:
    """Returns products with given manufacturer id"""
    products = Products.objects.filter(manufacturer_id=id)
    serializer = ProductsSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_product(request: Request, id: int) -> Response:
    """Return products with given id"""
    product = get_object_or_404(Products, id=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(["GET"])
def get_categories(request: Request) -> Response:
    """Returns list of categories"""
    categories = Categories.objects.all()
    print(categories)
    print(categories.first())
    serializer = CategoriesSerializer(categories, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_manufacturers(request: Request) -> Response:
    """Returns list of manufacturers"""
    manu = Manufacturers.objects.all()
    serializer = ManufacturersSerializer(manu, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_store(request: Request) -> Response:
    store = Store.objects.all()
    serializer = StoreSerializer(store, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_about(request: Request) -> Response:
    """Returns list with store info"""
    store = Store.objects.first()
    addresses = Addresses.objects.all()

    store_serializer = StoreSerializer(store)
    addresses_serializer = StoreSerializer(addresses, many=True)

    return Response(
        {"store": store_serializer.data, "addresses": addresses_serializer.data}
    )


# Not implemented
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_cart(request: Request, id: int) -> Response:
    product_info = request.query_params.get("product_info", "false").lower() == "true"
    user = request.user

    # Ensure the requested cart belongs to the authenticated user
    if user.id != int(id):
        return Response(
            {"detail": "Unauthorized access."}, status=status.HTTP_403_FORBIDDEN
        )

    orders = Orders.objects.filter(client__id=id, status="pending")

    # Serialize the cart content
    serializer = CartSerializer(
        orders, many=True, context={"product_info": product_info}
    )
    return Response(serializer.data)
