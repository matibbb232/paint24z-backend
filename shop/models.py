from django.db import models


class Test(models.Model):
    nazwa = models.CharField(max_length=100)

    class Meta:
        db_table = "test"


class OrderStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    SHIPPED = "shipped", "Shipped"
    DELIVERED = "delivered", "Delivered"


class Gender(models.TextChoices):
    FEMALE = "F", "Female"
    MALE = "M", "Male"


class Store(models.Model):
    name = models.CharField(max_length=30)
    email_address = models.EmailField(max_length=30)
    phone_number = models.CharField(max_length=15)
    tax_id = models.PositiveIntegerField()  # Assuming this is integer(10)

    class Meta:
        db_table = "store"


class Employees(models.Model):
    name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    pesel = models.CharField(max_length=11, blank=True, null=True)
    hire_date = models.DateField()
    email_address = models.EmailField(max_length=30)
    phone_number = models.CharField(max_length=15)
    bank_account_number = models.CharField(max_length=26, blank=True, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    class Meta:
        db_table = "Employees"


class Administrators(models.Model):
    employee = models.OneToOneField(Employees, on_delete=models.CASCADE)

    class Meta:
        db_table = "Administrators"


class Operators(models.Model):
    employee = models.OneToOneField(Employees, on_delete=models.CASCADE)

    class Meta:
        db_table = "Operators"


class Clients(models.Model):
    email_address = models.EmailField(max_length=30)
    phone_number = models.CharField(max_length=15)
    name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=Gender.choices)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    class Meta:
        db_table = "Clients"


class Addresses(models.Model):
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    building_number = models.CharField(max_length=5)
    apartment_number = models.CharField(max_length=4, blank=True, null=True)
    postal_code = models.CharField(max_length=6)
    warehouse = models.ForeignKey("Warehouses", on_delete=models.CASCADE)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)

    class Meta:
        db_table = "Addresses"


class Orders(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # For money type
    status = models.CharField(max_length=9, choices=OrderStatus.choices)
    order_date = models.DateField()
    shipping_date = models.DateField()
    history = models.TextField(blank=True, null=True)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)

    class Meta:
        db_table = "Orders"


class OrderDetails(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey("Products", on_delete=models.CASCADE)

    class Meta:
        db_table = "Order_Details"

class Manufacturers(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        db_table = "manufacturers"

class Products(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places = 5)
    composition = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=10, decimal_places = 5)
    store_id = models.IntegerField()
    # manufacturers_id = models.IntegerField()
    manufacturer = models.ForeignKey(
        Manufacturers,  # Reference the Manufacturers model
        on_delete=models.CASCADE,
        related_name="products",
        db_column="manufacturers_id"  # Map to the existing column name
    )
    categories_id = models.IntegerField()
    storage_spaces_id = models.IntegerField()
    class Meta:
        db_table = "products"


class Categories(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        db_table = "categories"




class Warehouses(models.Model):
    capacity = models.PositiveIntegerField()
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE)

    class Meta:
        db_table = "warehouses"


class StorageSpaces(models.Model):
    warehouses_id = models.ForeignKey(Warehouses, on_delete=models.CASCADE)

    class Meta:
        db_table = "storage_spaces"


class Users(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=50)
    creation_date = models.DateField()
    employee = models.ForeignKey(
        Employees, on_delete=models.CASCADE, blank=True, null=True
    )
    client = models.ForeignKey(Clients, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = "Users"
