from django.shortcuts import render, redirect
from bookstore_api.models import *
from django.urls import reverse
from django.db import transaction


import datetime
import re

from .views_add import addEdit_views_wrapper



def convert_field_name(field_name):
    words = re.findall('[A-Z][a-z0-9]*|[a-z]+', field_name)
    converted_name = ' '.join(words)

    words = converted_name.split()
    for i in range(len(words)):
        words[i] = words[i].capitalize()
    converted_name = ' '.join(words)
    return converted_name


def home_view(request):
    tmp_context = {
        'urls': ['book', 'publisher', 'transaction', 'writer', 'address', 'customer', 'inventory', 'payment', 'staff', 'store'],
        
    }
    context = {'data' : [{'url': f'{tmp_context["urls"][i]}', 'data': convert_field_name(tmp_context['urls'][i])} for i in range(len(tmp_context['urls']))]  }
    return render(request, 'home.html', context)

def key_to_db_obj():
    data = {'publisher': Publisher,
            'book': Book,
            'transaction': Transaction,
            'writer': Writer,
            'customer': Customer,
            'staff': Staff,
            'store': Store,
            'inventory': Inventory,
            }
    return data


def view_data(request, token):
    data = key_to_db_obj()

    obj = data[token].objects.select_related().all()

    field_names = [str(field.name) for field in data[token]._meta.get_fields()]

    related_field_names = []

    for field in data[token]._meta.get_fields():
        if field.is_relation and field.name != 'id':
            related_field_names.append(field.name)
    named_field_names = [convert_field_name(name) for name in field_names[1:]]
    combined_field_name = zip(field_names[1:], named_field_names)
    context = {
        'name': [token, convert_field_name(token)],
        'field_names': combined_field_name,
        'data': [],
        'id': [],
        
    }

    for data_obj in obj:
        row = []
        for field in field_names[1:]:
            if field in related_field_names:
                related_data = getattr(data_obj, field)
                if related_data:
                    related_value = getattr(related_data, field)
                    row.append(str(related_value))
                else:
                    row.append('N/A')
            else:
                value = getattr(data_obj, field)
                row.append(str(value))
        context['data'].append(row)
        context['id'].append(row[0])

    return render(request, "view_data.html", context)


@transaction.atomic
def delete_confirm(request, token, id):
    print(f'id: {id}')
    data = key_to_db_obj()
    if request.method == 'POST':
        obj = data[token].objects.get(pk=int(id))
        obj.delete()
        return redirect(f'/view_data/{token}')  # Redirect to the list of all data
    else:
        obj = data[token].objects.get(pk=int(id))
        context = {'obj_name': token,
                   'name': convert_field_name(token),
                   'obj': obj,
                   'id': id}
        return render(request, 'delete_confirm.html', context['obj'])


# @transaction.atomic
# def edit_confirm(request, token, id):
#     data = key_to_db_obj()
#     if request.method == 'POST':
#         obj = data[token].objects.get(pk=id)
#         for field in data[token]._meta.get_fields():
#             field_name = field.name
#             if field_name in request.POST:
#                 setattr(obj, field_name, request.POST[field_name])
#         # Update other fields if needed
#         obj.save()
#         return redirect(f'view_data/{token}')   # Redirect to the list of all data
#     else:
#         obj = data[token].objects.get(pk=id)
#         field_names = [str(field.name) for field in data[token]._meta.get_fields()]
#         named_field_names = [convert_field_name(name) for name in field_names[1:]]
#         objs = []
#         combined_field_name = zip(field_names[1:], named_field_names, objs)
#         context = {'obj_name': token,
#                    'name': convert_field_name(token),
#                    'obj': obj,
#                    'id': id,
#                    'field_names': combined_field_name}
#         return render(request, 'edit_confirm.html', context)


@transaction.atomic
def edit_confirm(request, token, id):
    if request.method == 'POST':
        id = int(id)
        response = addEdit_views_wrapper(token, request, type='edit', id=id)
        if response:
            return redirect(f'/view_data/{token}')
    else:
        return render(request, f'add_{token}.html', {'type_name': 'Edit', 'type': 'edit', 'id': str(id), 'urls': f'edit_data/{token}/{id}'})

def addData(request, token):
    if request.method == 'POST':
        response = addEdit_views_wrapper(token, request, type='add')
        if response:
            return redirect(f'/view_data/{token}')
    else:
        return render(request, f'add_{token}.html', {'type_name': 'Add', 'type': 'add', 'id':'add', 'urls': f'add_data/{token}'})



# def all_writer(request):

#     writer_obj = Writer.objects.filter()

#     context = {

#         "writer": writer_obj,

#     }

#     return render(request, "all_writer.html", context)

# def all_publisher(request):

#     publisher_obj = Publisher.objects.filter()

#     context = {

#         "publisher": publisher_obj,

#     }

#     return render(request, "all_publisher.html", context)




# def delete_publisher_confirm(request, publisher_id):
#     if request.method == 'POST':
#         publisher = Publisher.objects.get(pk=publisher_id)
#         publisher.delete()
#         return redirect('all_publisher')  # Redirect to the list of all publishers
#     else:
#         publisher = Publisher.objects.get(pk=publisher_id)
#         return render(request, 'delete_publisher.html', {'publisher': publisher})


# def edit_publisher_confirm(request, publisher_id):
#     if request.method == 'POST':
#         publisher = Publisher.objects.get(pk=publisher_id)
#         publisher.publisherName = request.POST['publisher_name']
#         publisher.publisherLocation = request.POST['publisher_location']
#         # Update other fields if needed
#         publisher.save()
#         return redirect('all_publisher')  # Redirect to the list of all publishers
#     else:
#         publisher = Publisher.objects.get(pk=publisher_id)
#         return render(request, 'edit_publisher.html', {'publisher': publisher})