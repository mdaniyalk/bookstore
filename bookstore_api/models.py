from django.db import models
from django.db.models import CharField

class Address(models.Model):
    addressId = models.AutoField(primary_key=True)
    streetName = models.TextField()
    buildingNum = models.IntegerField()
    regency = models.TextField()
    state = models.TextField()
    class Meta:
        db_table = 'address'

class Staff(models.Model):
    staffId = models.AutoField(primary_key=True)
    name = models.TextField()
    addressId = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    phoneNum = models.TextField()
    email = models.TextField()
    username = models.TextField()
    password = models.TextField()
    class Meta:
        db_table = 'staff'

class Customer(models.Model):
    customerId = models.AutoField(primary_key=True)
    name = models.TextField()
    addressId = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    phoneNum = models.TextField()
    email = models.TextField()
    class Meta:
        db_table = 'customer'   
    
class Publisher(models.Model):
    publisherId = models.AutoField(primary_key=True)
    publisherName = models.TextField()
    publisherLocation = models.TextField()
    class Meta:
        db_table = 'publisher'

class Writer(models.Model):
    writerId = models.AutoField(primary_key=True)
    writerName = models.TextField()
    class Meta:
        db_table = 'writer'

class Book(models.Model):
    bookId = models.AutoField(primary_key=True)
    title = models.TextField()
    descriptions = models.TextField()
    yearPublished = models.DateTimeField(null=True)
    publisherId = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True)
    writerId = models.ForeignKey(Writer, on_delete=models.SET_NULL, null=True)
    bookEdition = models.IntegerField()
    class Meta:
        db_table = 'book'  
    
class Store(models.Model):
    storeId = models.AutoField(primary_key=True)
    staffId = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    addressId = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table = 'store'

class Inventory(models.Model):
    inventoryId = models.AutoField(primary_key=True)
    storeId = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True)
    bookId = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True) 
    class Meta:
        db_table = 'inventory'

class Payment(models.Model):
    paymentId = models.AutoField(primary_key=True)
    method = models.TextField()
    value = models.FloatField()
    staffId = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table = 'payment'

class Transaction(models.Model):
    transactionId = models.AutoField(primary_key=True)
    time = models.DateTimeField(null=True)
    paymentId = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    customerId = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    inventoryId = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table = 'transaction'



