from django.shortcuts import render, reverse
from django.contrib.flatpages.models import FlatPage
from .models import TicketCar, TicketItem, TicketService, Profile, Seller
from django.conf import settings
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from .forms import ProfileForm, TicketCarForm, TicketItemForm, TicketServiceForm
from django.core import serializers


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

class BaseView():

    def base_queryset(self, model_name):
        tag = self.request.GET.get('tag')

        if tag:
            return model_name.objects.filter(tag__id=tag)
        else:
            return model_name.objects.all()

    def base_get_tags(model_name):
        tags_list = model_name.objects.values_list('tag__name', 'tag__id')
        tags_list = set(tags_list)
        return tags_list

    def get_seller(self, form):
        user = self.request.user
        form.instance.seller = Seller.objects.get(user=user)
        return form


class CarList(ListView):
    model = TicketCar
    context_object_name = 'ticket_car_list'
    template_name = 'cars/ticket_car_list.html'
    paginate_by = 10

    def get_queryset(self):
        return BaseView.base_queryset(self, self.model)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags_list'] = BaseView.base_get_tags(self.model)
        return context

class CarDetailView(DetailView):
    model = TicketCar
    template_name = 'cars/ticket_car_detail.html'
    context_object_name = 'ticket_car_detail'


class CarCreateView(CreateView):
    model = TicketCar
    template_name = "cars/ticket_car_create_form.html"
    success_url = '/'
    form_class = TicketCarForm

    def form_valid(self, form):
        BaseView.get_seller(self, form)
        return super().form_valid(form)


class CarUpdateView(UpdateView):
    model = TicketCar
    template_name = "cars/ticket_car_update_form.html"
    success_url = '/'
    form_class = TicketCarForm


class ServiceList(ListView):
    model = TicketService
    context_object_name = "ticket_service_list"
    template_name = 'services/ticket_service_list.html'
    paginate_by = 10

    def get_queryset(self):
        return BaseView.base_queryset(self, self.model)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags_list'] = BaseView.base_get_tags(self.model)
        return context

class ServiceDetailView(DetailView):
    model = TicketService
    template_name = 'services/ticket_service_detail.html'
    context_object_name = 'ticket_service_detail'


class ServiceCreateView(CreateView):
    model = TicketService
    form_class = TicketServiceForm
    success_url = '/'
    template_name = 'services/ticket_service_create_form.html'

    def form_valid(self, form):
        BaseView.get_seller(self, form)
        return super().form_valid(form)



class ServiceUpdateView(UpdateView):
    model = TicketService
    form_class = TicketServiceForm
    template_name = 'services/ticket_service_update_form.html'
    success_url = '/'




class ItemList(ListView):
    model = TicketItem
    context_object_name = "ticket_item_list"
    template_name = 'items/ticket_item_list.html'
    paginate_by = 10

    def get_queryset(self):
        return BaseView.base_queryset(self, self.model)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags_list'] = BaseView.base_get_tags(self.model)
        return context


class ItemDetailView(DetailView):
    model = TicketItem
    template_name = 'items/ticket_item_detail.html'
    context_object_name = "ticket_item_detail"


class ItemCreateView(CreateView):
    model = TicketItem
    form_class = TicketItemForm
    success_url = '/'
    template_name = 'items/ticket_item_create_form.html'

    def form_valid(self, form):
        BaseView.get_seller(self, form)
        return super().form_valid(form)


class ItemUpdateView(UpdateView):
    model = TicketItem
    form_class = TicketItemForm
    template_name = 'items/ticket_item_update_form.html'
    success_url = '/'


class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name_suffix = '_update_form'
    success_url = '/'
