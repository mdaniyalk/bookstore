from django.db import models

class IDPrimaryKey(models.CharField):
    def __init__(self, prefix='', *args, **kwargs):
        kwargs['max_length'] = 12
        kwargs['primary_key'] = True
        kwargs.setdefault('default', self.generate_default_value)
        super().__init__(*args, **kwargs)
        self.prefix = prefix

    def generate_default_value(self):
        # Generate the default primary key value
        last_obj = self.model.objects.order_by('-id').first()
        if last_obj:
            last_id = int(last_obj.id[len(self.prefix):])
            new_id = last_id + 1
        else:
            new_id = 1
        return f'{self.prefix}{new_id:05}'

    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        if not value:
            return self.generate_default_value()
        return value

class Address(models.Model):
    addressId = IDPrimaryKey(prefix='Add')
    streetName = models.TextField()
    buildingNum = models.IntegerField()
    regency = models.TextField()
    state = models.TextField()
    class Meta:
        db_table = 'address'

class Staff(models.Model):
    staffId = IDPrimaryKey(prefix='Sta')
    name = models.TextField()
    addressId = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    phoneNum = models.TextField()
    email = models.TextField()
    username = models.TextField()
    password = models.TextField()
    class Meta:
        db_table = 'staff'

class Customer(models.Model):
    customerId = IDPrimaryKey(prefix='Cus')
    name = models.TextField()
    addressId = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    phoneNum = models.TextField()
    email = models.TextField()
    class Meta:
        db_table = 'customer'   
    
class Publisher(models.Model):
    publisherId = IDPrimaryKey(prefix='Pub')
    publisherName = models.TextField()
    publisherLocation = models.TextField()
    class Meta:
        db_table = 'publisher'

class Writer(models.Model):
    writerId = IDPrimaryKey(prefix='Wri')
    writerName = models.TextField()
    class Meta:
        db_table = 'writer'

class Book(models.Model):
    bookId = IDPrimaryKey(prefix='Boo')
    title = models.TextField()
    descriptions = models.TextField()
    yearPublished = models.DateTimeField(null=True)
    publisherId = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True)
    writerId = models.ForeignKey(Writer, on_delete=models.SET_NULL, null=True)
    bookEdition = models.IntegerField()
    class Meta:
        db_table = 'book'  
    
class Store(models.Model):
    storeId = IDPrimaryKey(prefix='Sto')
    staffId = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    addressId = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table = 'store'

class Inventory(models.Model):
    inventoryId = IDPrimaryKey(prefix='Inv')
    storeId = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True)
    bookId = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True) 
    class Meta:
        db_table = 'inventory'

class Payment(models.Model):
    paymentId = IDPrimaryKey(prefix='Pym')
    method = models.TextField()
    value = models.FloatField()
    staffId = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table = 'payment'

class Transaction(models.Model):
    transactionId = IDPrimaryKey(prefix='Sto')
    time = models.DateTimeField(null=True)
    paymentId = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    customerId = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    inventoryId = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table = 'transaction'



