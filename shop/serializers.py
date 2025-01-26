from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
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
    Users,
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
    class Meta:
        model = Orders
        fields = "__all__"


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



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        # Check user existence
        try:
            user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            raise serializers.ValidationError("Invalid username or password.")

        if not user.check_password(password):  # Hash comparison
            raise serializers.ValidationError("Invalid username or password.")

        return super().validate(attrs)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer