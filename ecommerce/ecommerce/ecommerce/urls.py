"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from main.views import IndexView
from django.contrib.flatpages.views import flatpage
from main.views import CarList, ServiceList, ItemList, CarDetailView, ServiceDetailView, ItemDetailView, ProfileUpdateView,\
CarCreateView, ItemCreateView, ServiceCreateView, CarUpdateView, ItemUpdateView, ServiceUpdateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView, name='index'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('about/', flatpage, {'url': '/about/'}, name='about'),
    path('contacts/', flatpage, {'url': '/contacts/'}, name='contacts'),
    path('cars/', CarList.as_view(), name='car_list'),
    path('cars/add/', CarCreateView.as_view(), name='car_add'),
    path('cars/<int:pk>/', CarDetailView.as_view(), name='car_detail'),
    path('cars/<int:pk>/edit/', CarUpdateView.as_view(), name='car_detail_edit'),
    path('items/', ItemList.as_view(), name='item_list'),
    path('items/add/', ItemCreateView.as_view(), name='item_add'),
    path('items/<int:pk>/', ItemDetailView.as_view(), name='item_detail'),
    path('items/<int:pk>/edit/', ItemUpdateView.as_view(), name='item_detail_edit'),
    path('services/', ServiceList.as_view(), name='service_list'),
    path('services/add/', ServiceCreateView.as_view(), name='service_add'),
    path('services/<int:pk>/', ServiceDetailView.as_view(), name='service_detail'),
    path('services/<int:pk>/edit/', ServiceUpdateView.as_view(), name='service_detail_edit'),
    path('accounts/profile/<int:pk>/', ProfileUpdateView.as_view(), name='profile_update'),
]
