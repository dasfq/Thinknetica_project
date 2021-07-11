from django.shortcuts import render, reverse
from django.contrib.flatpages.models import FlatPage
from django.conf import settings
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .forms import ProfileForm, TicketCarForm, TicketItemForm, TicketServiceForm, PictureFormSet, CarFormSet
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import model_to_dict
from django.core.cache import caches
import random
from main.models import TicketCar, TicketItem, TicketService, Profile, Seller, Picture, SMSLog
from main.tasks import test1, test2, test3, send_notification, send_sms_phone_confirm
from main.asserts.generators import generate_cache_key

class DetailView(DetailView):
    '''Общая detailview для всех объявлений'''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = context['object']
        cache = caches['default']
        if obj.price:
            new_price = round(obj.price * random.uniform(0.8, 1.2))
            cache_key = generate_cache_key(obj)
            cache_price = cache.get_or_set(cache_key, new_price, 60)
            context['object'].price = cache_price
        return context


def IndexView(request):
    template_name = 'index.html'
    queryset = FlatPage.objects.all()
    test3.delay()
    test1.delay()
    test2.delay()
    context = {
        'pages': queryset,
        'user': request.user,
        'turn_on_block': settings.MAINTENANCE_MODE
    }
    return render(request, template_name,context)


@method_decorator(cache_page(settings.CACHE_TIMEOUT), name='dispatch')
class BaseView(View):
    '''Общий класс для всех ListView, через который применяется кэширование'''

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


class CarList(ListView, BaseView):
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
    template_name = "cars/ticket_car_create_update.html"
    success_url = '/'
    form_class = TicketCarForm

    def form_valid(self, form):
        """ получаем Seller и сохраняем форму """
        BaseView.get_seller(self, form)
        self.object = form.save(commit=False)

        ''' создаём форму и кладём в неё картинку'''
        if self.request.POST:
            pictures = PictureFormSet(self.request.POST, self.request.FILES, instance=self.object)

            """ провека валидности формсета. Соединяем обычную форму form и формсет с картинкой """
            if pictures.is_valid():
                pictures.instance = form.save()
                pictures.save()

        """ возвращаем обычную форму с присоединённым формсетом картинки"""
        return super(CarCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inline_formset'] = PictureFormSet()
        return context


class CarUpdateView(UpdateView):
    model = TicketCar
    template_name = "cars/ticket_car_create_update.html"
    success_url = '/'
    form_class = TicketCarForm

    def form_valid(self, form):
        self.object = form.save()

        if self.request.POST:
            pictures = PictureFormSet(self.request.POST, self.request.FILES, instance=self.object)

        """ form.is_valid() проверять не нужно, так как она уже вызвана в self.post(), который уже, в случае успешной
        валидации, и запускает self.form_valid()"""
        if pictures.is_valid():
            pictures.save()

        return super(CarUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['picture_formset'] = PictureFormSet()
        return context


class ServiceList(ListView, BaseView):
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


class ItemList(ListView, BaseView):
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


class ItemCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'main.TicketItem_all'
    model = TicketItem
    form_class = TicketItemForm
    success_url = '/'
    template_name = 'items/ticket_item_create_form.html'

    def form_valid(self, form):
        BaseView.get_seller(self, form)
        instance = model_to_dict(form.instance)
        send_notification.delay(instance)
        return super().form_valid(form)


class ItemUpdateView(UpdateView):
    model = TicketItem
    form_class = TicketItemForm
    template_name = 'items/ticket_item_update_form.html'
    success_url = '/'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name_suffix = '_update_form'

    def form_valid(self, form):
        phone = form.instance.phone_number
        print('form.instance.phone_number', phone)
        # profile = form.save(commit=False)
        if phone:
            response = send_sms_phone_confirm.delay(phone)
        return super().form_valid(form)