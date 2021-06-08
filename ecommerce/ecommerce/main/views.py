from django.shortcuts import render, reverse
from django.contrib.flatpages.models import FlatPage
from .models import TicketCar, TicketItem, TicketService, Profile
from django.conf import settings
from django.views.generic import ListView, DetailView, UpdateView
from .forms import ProfileForm


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

class BaseListView():

    def base_queryset(self, model_name):
        tag = self.request.GET.get('tag')

        if tag:
            return model_name.objects.filter(tag__id=tag)
        else:
            return model_name.objects.all()

    def base_get_tags(model_name):
        tags_list = []
        for ticket in model_name.objects.all():
            for tag in ticket.tag.all():
                tags_list.append(tag)
        tags_list = set(tags_list)
        return tags_list

class CarList(ListView):
    model = TicketCar
    context_object_name = 'ticket_car_list'
    template_name = 'ticket_car_list.html'
    paginate_by = 10

    def get_queryset(self):
        return BaseListView.base_queryset(self, self.model)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags_list'] = BaseListView.base_get_tags(self.model)
        return context

class CarDetailView(DetailView):
    model = TicketCar
    template_name = 'ticket_car_detail.html'
    context_object_name = 'ticket_car_detail'


class ServiceList(ListView):
    model = TicketService
    context_object_name = "ticket_service_list"
    template_name = 'ticket_service_list.html'
    paginate_by = 10

    def get_queryset(self):
        return BaseListView.base_queryset(self, self.model)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags_list'] = BaseListView.base_get_tags(self.model)
        return context

class ServiceDetailView(DetailView):
    model = TicketService
    template_name = 'ticket_service_detail.html'
    context_object_name = 'ticket_service_detail'


class ItemList(ListView):
    model = TicketItem
    context_object_name = "ticket_item_list"
    template_name = 'ticket_item_list.html'
    paginate_by = 10

    def get_queryset(self):
        return BaseListView.base_queryset(self, self.model)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags_list'] = BaseListView.base_get_tags(self.model)
        return context

class ItemDetailView(DetailView):
    model = TicketItem
    template_name = 'ticket_item_detail.html'
    context_object_name = "ticket_item_detail"

class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name_suffix = '_update_form'
    # fields = ('birth_date',)
    success_url = '/'
