"""transfer_data URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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

from django.urls import path

from . import views

urlpatterns = [
    path('transfer',views.TransferData),
    path('inventory',views.InventoryView,name='inventory'),
    path('inventory_per',views.InventoryPerView,name='inventory_per'),
    path('inventory_ajax',views.InventoryAjax,name='inventory_ajax'),
    path('inventory_per_ajax',views.InventoryPerAjax,name='inventory_per_ajax'),
    path('',views.IndexView,name='index'),

]
