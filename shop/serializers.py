from rest_framework import serializers
from shop.models import (
    Products,
    Categories,
    Store,
    Addresses,
    Orders,
    OrderDetails,
    Clients,
    Warehouses,
    StorageSpaces,
    Manufacturers,
    Test,
)


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = "__all__"


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = "__all__"


class ManufacturersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturers
        fields = "__all__"


class ProductsSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturersSerializer()
    category = CategoriesSerializer()

    class Meta:
        model = Products
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    manufacturer = ManufacturersSerializer()

    class Meta:
        model = Products
        fields = "__all__"


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"


class StorageSpacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageSpaces
        fields = "__all__"


class WarehousesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouses
        fields = "__all__"


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addresses
        fields = [
            "country",
            "city",
            "street",
            "building_number",
            "apartment_number",
            "postal_code",
        ]


class OrdersSerializer(serializers.ModelSerializer):
    client_name = serializers.StringRelatedField(source="client.name")

    class Meta:
        model = Orders
        fields = [
            "id",
            "amount",
            "status",
            "order_date",
            "shipping_date",
            "history",
            "client_name",
        ]


class OrderDetailsSerializer(serializers.ModelSerializer):
    product_name = serializers.StringRelatedField(source="product.name")

    class Meta:
        model = OrderDetails
        fields = ["id", "order", "product", "product_name"]


class ClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = [
            "id",
            "email_address",
            "phone_number",
            "name",
            "last_name",
            "gender",
            "store",
        ]


class CartSerializer(serializers.ModelSerializer):
    product_details = OrderDetailsSerializer(source="orderdetails_set", many=True)

    class Meta:
        model = Orders
        fields = ["id", "product_details"]
