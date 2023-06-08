"""bookstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from bookstore_api.views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('add_writer/', addWriter, name='add_writer'),
    path('add_writer', addWriter, name='add_writer_post'),
    path('add_book/', addBook, name='add_book'),
    path('add_book', addBook, name='add_book_post'),
    path('add_publisher/', addPublisher, name='add_publisher'),
    path('add_publisher', addPublisher, name='add_publisher_post'),
    path('add_transaction/', addTransaction, name='add_transaction'),
    path('add_transaction', addTransaction, name='add_transaction_post'),

    path('all_writer/', all_writer, name='all_writer'),
    path('all_publisher/', all_publisher, name='all_publisher'),
]
