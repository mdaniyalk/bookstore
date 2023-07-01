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
from bookstore_api.views_add import *

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('writer/<str:type>/', addEditWriter, name='writer'),
    path('writer/<str:type>', addEditWriter, name='writer_post'),
    path('book/<str:type>/', addEditBook, name='book'),
    path('book/<str:type>', addEditBook, name='book_post'),
    path('publisher/<str:type>/', addEditPublisher, name='publisher'),
    path('publisher/<str:type>', addEditPublisher, name='publisher_post'),
    path('transaction/<str:type>/', addEditTransaction, name='transaction'),
    path('transaction/<str:type>', addEditTransaction, name='transaction_post'),

    # path('delete_publisher_confirm/<int:publisher_id>/', delete_publisher_confirm, name='delete_publisher_confirm'),
    # path('edit_publisher_confirm/<int:publisher_id>/', edit_publisher_confirm, name='edit_publisher_confirm'),

    # path('all_writer/', all_writer, name='all_writer'),
    # path('all_publisher/', all_publisher, name='all_publisher'),
    path('view_data/<str:token>', view_data, name='view_data'),
    path('view_data/<str:token>/', view_data, name='view_data'),
    path('edit_data/<str:token>/', edit_confirm, name='edit_data'),
    path('edit_data/<str:token>', edit_confirm, name='edit_data'),
    path('edit_data/<str:token>/<int:id>', edit_confirm, name='edit_data'),
    path('edit_data/<str:token>/<int:id>/', edit_confirm, name='edit_data'),
    path('delete_confirm/<str:token>/<int:id>', delete_confirm, name='delete_confirm'),
    path('delete_confirm/<str:token>/<int:id>/', delete_confirm, name='delete_confirm'),
    path('add_data/<str:token>', addData, name='add_data'),
    path('add_data/<str:token>/', addData, name='add_data'),


]
