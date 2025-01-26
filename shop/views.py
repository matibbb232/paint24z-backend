from typing import Type

from django.contrib.auth.hashers import make_password
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework import authentication, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    AllowAny,
    BasePermission,
    IsAdminUser,
    IsAuthenticated,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Addresses,
    Categories,
    Manufacturers,
    OrderDetails,
    Orders,
    Products,
    Store,
    Users,
)
from .serializers import (
    CategoriesSerializer,
    ManufacturersSerializer,
    OrderDetailsSerializer,
    OrdersSerializer,
    ProductSerializer,
    ProductsSerializer,
    ProductQuantitySerializer,
    StoreSerializer,
)


## todo: add authentication and adding client id from jwt, and putting it to db
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def make_order(request: Request) -> Response:
    """Function for posting order data"""
    username = request.user
    serializer = ProductQuantitySerializer(data=request.data, many=True)
    print(username)
    Users.objects.filter(username=username)
    
    if serializer.is_valid():
        # Process the valid data
        product_data = serializer.validated_data

        print(product_data)

        # Example: You could save the data, calculate totals, etc.
        # For now, let's just return the received data
        return Response(
            {"message": "Products processed successfully.", "data": product_data},
            status=status.HTTP_200_OK,
        )

    # Return errors if validation fails
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_orders(request: Request) -> Response:
    """Returns list of all orders"""

    orders = Orders.objects.all()
    serializer = OrdersSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_products(request: Request) -> Response:
    """Returns list of products with optional filtering and sorting."""
    category_id: str | None = request.query_params.get("category")
    manufacturer_id: str | None = request.query_params.get("manufacturer")
    sort_by: str = request.query_params.get("sort_by", "id")  # default value "id"
    order: str = request.query_params.get("order", "asc").lower()  # default value "asc"

    filters: dict[str, int] = {}

    # FIXME: Should be removed in final vesion!
    hashed_password = make_password("kochamkable123")
    print(hashed_password)
    print("securePass456: " + make_password("securePass456"))
    print("admin789: " + make_password("admin789"))
    print("LOL123insecure: " + make_password("LOL123insecure"))

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

    if order == "desc":
        sort_by = f"-{sort_by}"  # Prefix with '-' for descending order
    elif order != "asc":
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
    """Returns list of stores"""
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


class IsClientOrAdmin(IsAuthenticated):
    """
    Custom permission to allow only the client with the given ID
    or an admin user to access the data.
    """

    def has_permission(self, request: Request, view: View) -> bool:
        # Ensure the user is authenticated
        if not super().has_permission(request, view):
            return False

        # Check if the user is an admin
        if request.user.is_staff:
            return True

        # Check if the user ID matches the client ID in the request
        users_id = view.kwargs.get("users_id")
        return str(request.user.id) == str(users_id)


class UserOrdersView(APIView):
    """Class for handling client orders"""

    permission_classes: list[Type[BasePermission]] = [IsClientOrAdmin]

    def get(self, request: Request, user_id: int) -> Response:
        """Returns orders of client"""
        # Fetch all orders for the given client_id
        orders: QuerySet[Orders] = Orders.objects.filter(users_id=user_id)

        if not orders.exists():
            return Response(
                {"detail": "No orders found for this client."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Serialize the orders
        orders_serializer = OrdersSerializer(orders, many=True)

        # Fetch all order details for the fetched orders
        order_details: QuerySet[OrderDetails] = OrderDetails.objects.filter(
            order__in=orders
        )

        # Serialize the order details
        order_details_serializer = OrderDetailsSerializer(order_details, many=True)

        # Combine the serialized data
        response_data: dict[str, list[dict]] = {
            "orders": orders_serializer.data,
            "order_details": order_details_serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)
