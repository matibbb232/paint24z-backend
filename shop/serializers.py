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
)

class ProductsSerializer(serializers.ModelSerializer):
    # category = serializers.StringRelatedField(source='categories_set.name', many=True)
    # manufacturer = serializers.StringRelatedField(source='manufacturers_set.name', many=True)

    class Meta:
        model = Products
        fields ='__all__'

# CREATE TABLE "Products"(
#   id integer NOT NULL,
#   "Name" varchar(100) NOT NULL,
#   "Description" text NOT NULL,
#   "Price" money NOT NULL,
#   "Composition" varchar(100) NOT NULL,
#   "Weight" NUMERIC(10, 2) NOT NULL,
#   "Store_id" integer NOT NULL,
#   "Manufacturers_id" integer NOT NULL,
#   CONSTRAINT "Products_pkey" PRIMARY KEY(id)
# );
class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(source='categories_set.name', many=True)
    manufacturer = serializers.StringRelatedField(source='manufacturers_set.name', many=True)

    class Meta:
        model = Products
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id', 'name', 'description']


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['name', 'email_address', 'phone_number', 'tax_id']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addresses
        fields = ['country', 'city', 'street', 'building_number', 'apartment_number', 'postal_code']


class OrdersSerializer(serializers.ModelSerializer):
    client_name = serializers.StringRelatedField(source='client.name')

    class Meta:
        model = Orders
        fields = ['id', 'amount', 'status', 'order_date', 'shipping_date', 'history', 'client_name']


class OrderDetailsSerializer(serializers.ModelSerializer):
    product_name = serializers.StringRelatedField(source='product.name')

    class Meta:
        model = OrderDetails
        fields = ['id', 'order', 'product', 'product_name']


class ClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = ['id', 'email_address', 'phone_number', 'name', 'last_name', 'gender', 'store']


class CartSerializer(serializers.ModelSerializer):
    product_details = OrderDetailsSerializer(source='orderdetails_set', many=True)

    class Meta:
        model = Orders
        fields = ['id', 'product_details']
