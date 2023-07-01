from django.core.management.base import BaseCommand
from bookstore_api.models import Address, Staff, Customer, Publisher, Writer, Book, Store, Inventory, Payment, Transaction
import random
from datetime import datetime, timedelta
from django.utils import timezone

def populate_tables():
    # Populate Address table
    addresses = []
    for _ in range(100):
        address = Address(
            streetName='Street ' + str(random.randint(1, 100)),
            buildingNum=random.randint(1, 100),
            regency='Regency ' + str(random.randint(1, 10)),
            state='State ' + str(random.randint(1, 5))
        )
        addresses.append(address)
    Address.objects.bulk_create(addresses)

    # Populate Staff table
    staff_members = []
    for _ in range(100):
        staff = Staff(
            name='Staff ' + str(random.randint(1, 100)),
            addressId=random.choice(addresses),
            phoneNum='Phone ' + str(random.randint(1, 100)),
            email='staff' + str(random.randint(1, 100)) + '@example.com',
            username='username' + str(random.randint(1, 100)),
            password='password' + str(random.randint(1, 100))
        )
        staff_members.append(staff)
    Staff.objects.bulk_create(staff_members)

    # Populate Customer table
    customers = []
    for _ in range(100):
        customer = Customer(
            name='Customer ' + str(random.randint(1, 100)),
            addressId=random.choice(addresses),
            phoneNum='Phone ' + str(random.randint(1, 100)),
            email='customer' + str(random.randint(1, 100)) + '@example.com'
        )
        customers.append(customer)
    Customer.objects.bulk_create(customers)

    # Populate Publisher table
    publishers = []
    for _ in range(100):
        publisher = Publisher(
            publisherName='Publisher ' + str(random.randint(1, 100)),
            publisherLocation='Location ' + str(random.randint(1, 10))
        )
        publishers.append(publisher)
    Publisher.objects.bulk_create(publishers)

    # Populate Writer table
    writers = []
    for _ in range(100):
        writer = Writer(
            writerName='Writer ' + str(random.randint(1, 100))
        )
        writers.append(writer)
    Writer.objects.bulk_create(writers)

    # Populate Book table
    books = []
    for _ in range(1000):
        book = Book(
            title='Book ' + str(random.randint(1, 100)),
            descriptions='Description ' + str(random.randint(1, 100)),
            yearPublished=timezone.now() - timedelta(days=random.randint(1, 365)),
            publisherId=random.choice(publishers),
            writerId=random.choice(writers),
            bookEdition=random.randint(1, 5)
        )
        books.append(book)
    Book.objects.bulk_create(books)

    # Populate Store table
    stores = []
    for _ in range(10):
        store = Store(
            staffId=random.choice(staff_members),
            addressId=random.choice(addresses)
        )
        stores.append(store)
    Store.objects.bulk_create(stores)

    # Populate Inventory table
    inventories = []
    for _ in range(100):
        inventory = Inventory(
            storeId=random.choice(stores),
            bookId=random.choice(books)
        )
        inventories.append(inventory)
    Inventory.objects.bulk_create(inventories)

    # Populate Payment table
    payments = []
    for _ in range(1000):
        payment = Payment(
            method='Payment Method ' + str(random.randint(1, 100)),
            value=random.uniform(10, 1000),
            staffId=random.choice(staff_members)
        )
        payments.append(payment)
    Payment.objects.bulk_create(payments)

    # Populate Transaction table
    transactions = []
    for _ in range(1000):
        transaction = Transaction(
            time=timezone.now() - timedelta(days=random.randint(1, 30)),
            paymentId=random.choice(payments),
            customerId=random.choice(customers),
            inventoryId=random.choice(inventories)
        )
        transactions.append(transaction)
    Transaction.objects.bulk_create(transactions)



class Command(BaseCommand):
    help = 'Populates the tables with random data'

    def handle(self, *args, **options):
        # Call the populate_tables function
        populate_tables()
        self.stdout.write(self.style.SUCCESS('Data population completed.'))
