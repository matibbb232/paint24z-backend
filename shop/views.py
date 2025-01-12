from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from .models import Products, Manufacturers, Categories, Store, Addresses, Orders, Test
from .serializers import (
    ProductsSerializer,
    CategoriesSerializer,
    StoreSerializer,
    CartSerializer,
    TestSerializer
)
from rest_framework.views import APIView
# from rest_framework.response import Response
from rest_framework import authentication, permissions
# from django.contrib.auth.models import User

# class Test(APIView):
# 	# permission_classes = (permissions.IsAuthenticated,)
# 	# authentication_classes = (SessionAuthentication,)
# 	##
# 	def get(self, request):
# 		serializer = TestSerializer(request.user)
# 		return Response({'user': serializer.data}, status=status.HTTP_200_OK)



@api_view(["GET"])
def get_test(request):
    car = Test.objects.all()
    print(car)
    product = get_object_or_404(Test, id=1)
    return Response(TestSerializer(product).data)

@api_view(["GET"])
def get_products(request):
    products = Products.objects.all()

    serializer = ProductsSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def test_json(request):
    # Hardcoded JSON data
    data = {
        "message": "Hello, this is a test JSON response!",
        "status": "success",
        "data": {
            "id": 1,
            "name": "Test Item",
            "description": "This is a hardcoded item for demonstration purposes.",
        },
    }
    return Response(data)


@api_view(["GET"])
def get_product(request, id):
    product_info = request.query_params.get("product_info", "false").lower() == "true"
    product = get_object_or_404(Products, id=id)

    # Selective serialization based on `product_info`
    if product_info:
        serializer = ProductsSerializer(product)
    else:
        serializer = ProductsSerializer(
            product, fields=("name", "price")
        )  # Only name and price

    return Response(serializer.data)


@api_view(["GET"])
def get_categories(request):
    categories = Categories.objects.all()
    print(categories)
    print(categories.first())
    serializer = CategoriesSerializer(categories, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_about(request):
    store = Store.objects.first()
    addresses = Addresses.objects.all()

    store_serializer = StoreSerializer(store)
    addresses_serializer = StoreSerializer(addresses, many=True)

    return Response(
        {"store": store_serializer.data, "addresses": addresses_serializer.data}
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_cart(request, id):
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
