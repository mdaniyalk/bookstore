from django.shortcuts import render
from bookstore_api.models import *

import datetime


def staff_detail(request, staffId):

    staff_obj = Staff.objects.get(staffId=staffId)
    address_obj = Address.objects.get(address_id = staff_obj.addressId)
    context = {

        "staff": staff_obj,
        "address": address_obj,

    }

    return render(request, "staff_detail.html", context)



def customer_detail(request, customerId):

    customer_obj = Customer.objects.get(customerId=customerId)
    address_obj = Address.objects.get(address_id = customer_obj.addressId)

    context = {

        "customer": customer_obj,
        "address": address_obj,

    }

    return render(request, "customer_detail.html", context)

def publisher_detail(request, publisherId):

    publisher_obj = Publisher.objects.get(publisherId=publisherId)

    context = {

        "publisher": publisher_obj,

    }

    return render(request, "publisher_detail.html", context)

def writer_detail(request, writerId):

    writer_obj = Writer.objects.get(writerId=writerId)

    context = {

        "writer": writer_obj,

    }

    return render(request, "writer_detail.html", context)

def book_detail(request, bookId):

    book_obj = Book.objects.get(bookId=bookId)
    writer_obj = Writer.objects.get(writerId=book_obj.writerId)
    publisher_obj = Publisher.objects.get(publisherId=book_obj.publisherId)

    context = {

        "book": book_obj,
        "writer": writer_obj,
        "publisher": publisher_obj,

    }

    return render(request, "book_detail.html", context)

def store_detail(request, storeId):

    store_obj = Store.objects.get(storeId=storeId)
    staff_obj = Staff.objects.get(staffId=store_obj.staffId)
    address_obj = Address.objects.get(address_id = store_obj.addressId)

    context = {

        "store": store_obj,
        "staff": staff_obj,
        "address": address_obj,

    }

    return render(request, "store_detail.html", context)

def transaction_detail(request, transactionId):

    transaction_obj = Transaction.objects.get(transactionId=transactionId)
    payment_obj = Payment.objects.get(paymentId=transaction_obj.paymentId)
    customer_obj = Customer.objects.get(customerId=transaction_obj.customerId)
    inventory_obj = Inventory.objects.get(inventoryId=transaction_obj.inventoryId)

    context = {

        "transaction": transaction_obj,
        "payment": payment_obj,
        "customer": customer_obj,
        "inventory": inventory_obj,

    }

    return render(request, "transaction_detail.html", context)

def get_cust_id(name, phone):
    try:
        user = Customer.objects.get(name=name, 
                                    bookId=phone)
        return user.customerId
    except Customer.DoesNotExist:
        return None

def get_book_id(title):
    try:
        book = Book.objects.get(title=title)
        return book.bookId
    except Book.DoesNotExist:
        return None    

def get_staff_id(name):
    try:
        staff = Staff.objects.get(name=name)
        return staff.staffId
    except staff.DoesNotExist:
        return None   

def get_inventory_id(storeId, bookId):
    try:
        inventory = Inventory.objects.get(storeId=storeId, 
                                          bookId=bookId)
        return inventory.inventoryId
    except Inventory.DoesNotExist:
        return None


def addTransaction(request):
    if request.method == 'POST':
        custName = request.POST['custName']
        custPhone = request.POST['custPhone']
        customerId = get_cust_id(custName, custPhone)
        item = request.POST['item']
        bookId = get_book_id(item)
        method = request.POST['method']
        value = float(request.POST['value'])
        time = datetime.datetime.now()
        storeId = request.POST['StoreId']
        staffName = request.POST['staffName']
        staffId = get_staff_id(staffName)

        inventoryId = get_inventory_id(storeId, bookId)

        Payment.objects.create(method=method, 
                               value=value, 
                               staffId=staffId)
        payment = Payment.objects.get(method=method, 
                                      value=value, 
                                      staffId=staffId)
        
        Transaction.objects.create(time=time, 
                                   paymentId=payment.paymentId, 
                                   customerId = customerId,
                                   inventoryId = inventoryId
                                   )
        return render(request, 'success.html')
    return render(request, 'add_transaction.html')