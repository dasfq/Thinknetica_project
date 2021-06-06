from django.shortcuts import render
from django.contrib.flatpages.models import FlatPage
from .models import TicketCar, TicketItem, TicketService
from django.conf import settings
from django.views.generic import ListView, DetailView


# Create your views here.

def IndexView(request):
    template_name = 'index.html'
    queryset = FlatPage.objects.all()
    context = {
        'pages': queryset,
        'user': request.user,
        'turn_on_block': settings.MAINTENANCE_MODE
    }
    return render(request, template_name,context)

class CarList(ListView):
    model = TicketCar
    context_object_name = 'ticket_car_list'
    template_name = 'ticket_car_list.html'



class ServiceList(ListView):
    model = TicketService
    context_object_name = "ticket_service_list"
    template_name = 'ticket_service_list.html'
class ItemList(ListView):
    model = TicketItem
    context_object_name = "ticket_item_list"
    template_name = 'ticket_item_list.html'