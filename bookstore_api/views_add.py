from django.shortcuts import render, redirect
from bookstore_api.models import *
from django.urls import reverse
from django.db import transaction


import datetime
import re



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
    except Staff.DoesNotExist:
        return None   

def get_inventory_id(storeId, bookId):
    try:
        inventory = Inventory.objects.get(storeId=storeId, 
                                          bookId=bookId)
        return inventory.inventoryId
    except Inventory.DoesNotExist:
        return None

def get_publisher_id(name):
    try:
        publisher = Publisher.objects.get(publisherName=name)
        return publisher.publisherId
    except Publisher.DoesNotExist:
        return None 
    
def get_writer_id(name):
    try:
        writer = Writer.objects.get(writerName=name)
        return writer.writerId
    except Writer.DoesNotExist:
        return None     

def get_datetime_from_year(year):
    datetime_value = datetime.datetime(int(year), 1, 1)
    return datetime_value


@transaction.atomic
def addEditTransaction(request, type, id):
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

        
        if type == 'add':
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
        elif type == 'edit':
            obj = Transaction.objects.get(pk=id)
            pym = Payment.objects.get(pk=obj.paymentId)
            obj.time=time
            obj.paymentId=payment.paymentId 
            pym.method=method
            pym.value=value, 
            pym.staffId=staffId
            pym.save()
            obj.customerId = customerId
            obj.inventoryId = inventoryId
            obj.save()
        return True
    return False


@transaction.atomic
def addEditBook(request, type, id):
    if request.method == 'POST':
        title = request.POST['title']
        descriptions = request.POST['descriptions']
        yearPublished = request.POST['yearPublished']
        yearPublished = get_datetime_from_year(yearPublished)
        publisher = request.POST['publisher']
        publisherId = get_publisher_id(publisher)
        writer = request.POST['writer']
        writerId = get_writer_id(writer)
        edition = int(request.POST['edition'])
        if type == 'add':
            Book.objects.create(title=title, 
                                descriptions=descriptions, 
                                yearPublished = yearPublished,
                                publisherId = publisherId,
                                writerId = writerId,
                                bookEdition = edition
                                )
        elif type == 'edit':
            obj = Book.objects.get(pk=id)
            obj.title=title 
            obj.descriptions=descriptions 
            obj.yearPublished = yearPublished
            obj.publisherId = publisherId
            obj.writerId = writerId
            obj.bookEdition = edition
            obj.save()
        return True
    return False


@transaction.atomic
def addEditPublisher(request, type, id):
    if request.method == 'POST':
        publisherName = request.POST['publisherName']
        publisherLocation = request.POST['publisherLocation']
        if type == 'add':
            Publisher.objects.create(publisherName = publisherName,
                                    publisherLocation = publisherLocation)
        elif type == 'edit':
            obj = Publisher.objects.get(pk=id)
            obj.publisherName = publisherName
            obj.publisherLocation = publisherLocation
            obj.save()
        return True
    return False



@transaction.atomic
def addEditWriter(request, type, id):
    if request.method == 'POST':
        writerName = request.POST['writerName']
        if type == 'add':
            Writer.objects.create(writerName=writerName)
        elif type == 'edit':
            obj = Writer.objects.get(pk=id)
            obj.writerName = writerName
            obj.save()
        return True
    return False





def addEdit_views_wrapper(token, request, type, id=None):
    if token == 'publisher': 
        response = addEditPublisher(request, type, id)
    elif token == 'book': 
        response = addEditBook(request, type, id)
    elif token == 'transaction': 
        response = addEditTransaction(request, type, id)
    elif token == 'writer':
        response = addEditWriter(request, type, id)
    elif token == 'customer':
        response = addEditCustomer(request, type, id)
    elif token == 'staff':
        response = addEditStaff(request, type, id)
    elif token == 'store':
        response = addEditStore(request, type, id)
    elif token == 'inventory':
        response = addEditInventory(request, type, id)
    return response