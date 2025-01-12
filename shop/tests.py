from django.test import TestCase
from shop.models import (
    Store,
    Employees,
    Administrators,
    Operators,
    Clients,
    Addresses,
    Orders,
    OrderDetails,
    Products,
    Categories,
    Manufacturers,
    Warehouses,
    StorageSpaces,
    Users,
    OrderStatus,
    Gender,
)
from datetime import date


class BaseTestCase(TestCase):
    def setUp(self):
        # Create a Store
        self.store = Store.objects.create(
            name="Test Store",
            email_address="store@example.com",
            phone_number="123456789",
            tax_id=1234567890,
        )

        # Create an Employee
        self.employee = Employees.objects.create(
            name="John",
            last_name="Doe",
            birth_date="1985-05-15",
            pesel="85051512345",
            hire_date="2020-01-01",
            email_address="employee@example.com",
            phone_number="987654321",
            bank_account_number="12345678901234567890123456",
            store=self.store,
        )

        # Create a Client
        self.client = Clients.objects.create(
            email_address="client@example.com",
            phone_number="111222333",
            name="Jane",
            last_name="Smith",
            gender=Gender.FEMALE,
            store=self.store,
        )

        # Create a Warehouse
        self.warehouse = Warehouses.objects.create(capacity=1000, store=self.store)

        # Create a Product
        self.product = Products.objects.create(
            name="Product 1",
            description="A test product",
            price=99.99,
            composition=80,
            weight=1.5,
            store=self.store,
        )


class StoreModelTests(BaseTestCase):
    def test_store_creation(self):
        self.assertEqual(Store.objects.count(), 1)
        self.assertEqual(self.store.name, "Test Store")

    def test_store_deletion(self):
        self.store.delete()
        self.assertEqual(Store.objects.count(), 0)


class EmployeeModelTests(BaseTestCase):
    def test_employee_creation(self):
        self.assertEqual(Employees.objects.count(), 1)
        self.assertEqual(self.employee.name, "John")
        self.assertEqual(self.employee.store, self.store)

    def test_employee_deletion(self):
        self.employee.delete()
        self.assertEqual(Employees.objects.count(), 0)


class ClientModelTests(BaseTestCase):
    def test_client_creation(self):
        self.assertEqual(Clients.objects.count(), 1)
        self.assertEqual(self.client.name, "Jane")

    def test_client_deletion(self):
        self.client.delete()
        self.assertEqual(Clients.objects.count(), 0)


class OrderModelTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.order = Orders.objects.create(
            amount=199.99,
            status=OrderStatus.PENDING,
            order_date=date.today(),
            shipping_date=date.today(),
            client=self.client,
        )

    def test_order_creation(self):
        self.assertEqual(Orders.objects.count(), 1)
        self.assertEqual(self.order.amount, 199.99)
        self.assertEqual(self.order.client, self.client)

    def test_order_deletion(self):
        self.order.delete()
        self.assertEqual(Orders.objects.count(), 0)


class ProductAndCategoryTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.category = Categories.objects.create(
            name="Test Category",
            description="Category description",
            product=self.product,
        )

    def test_product_creation(self):
        self.assertEqual(Products.objects.count(), 1)
        self.assertEqual(self.product.name, "Product 1")


#     def test_category_creation(self):
#         self.assertEqual(Categories.objects.count(), 1)
#         self.assertEqual(self.category.name, "Test Category")

#     def test_product_deletion_cascades_to_category(self):
#         self.product.delete()
#         self.assertEqual(Categories.objects.count(), 0)

# class WarehouseAndStorageSpaceTests(BaseTestCase):
#     def setUp(self):
#         super().setUp()
#         self.storage_space = StorageSpaces.objects.create(
#             product=self.product,
#             warehouse=self.warehouse
#         )

#     def test_warehouse_creation(self):
#         self.assertEqual(Warehouses.objects.count(), 1)
#         self.assertEqual(self.warehouse.capacity, 1000)

#     def test_storage_space_creation(self):
#         self.assertEqual(StorageSpaces.objects.count(), 1)
#         self.assertEqual(self.storage_space.product, self.product)

#     def test_warehouse_deletion_cascades_to_storage_space(self):
#         self.warehouse.delete()
#         self.assertEqual(StorageSpaces.objects.count(), 0)
