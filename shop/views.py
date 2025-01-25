from django.db.models.query import QuerySet
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
    """Returns list of products with optional filtering and sorting."""
    category_id: str | None = request.query_params.get("category")
    manufacturer_id: str | None = request.query_params.get("manufacturer")
    sort_by: str = request.query_params.get("sort_by", "id")  # Default sorting by 'id'
    order: str = request.query_params.get("order").lower()

    filters: dict[str, int] = {}

    if category_id:
        try:
            filters["category_id"] = int(category_id)
        except ValueError:
            return Response(
                {"error": "Invalid category ID. Must be an integer."}, status=400
            )

    if manufacturer_id:
        try:
            filters["manufacturer_id"] = int(manufacturer_id)
        except ValueError:
            return Response(
                {"error": "Invalid manufacturer ID. Must be an integer."}, status=400
            )

    valid_sort_fields: list[str] = [
        "id",
        "name",
        "price",
        "weight",
    ]
    if sort_by not in valid_sort_fields:
        return Response(
            {
                "error": f"Invalid sort_by field. Allowed fields: {', '.join(valid_sort_fields)}."
            },
            status=400,
        )

    if order.lower() == "desc":
        sort_by = f"-{sort_by}"  # Prefix with '-' for descending order
    elif order.lower() != "asc":
        return Response(
            {"error": "Invalid order value. Must be 'asc' or 'desc'."}, status=400
        )

    products: QuerySet = Products.objects.filter(**filters).order_by(sort_by)

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
