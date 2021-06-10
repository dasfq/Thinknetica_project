from django import forms
from .models import Profile, TicketCar, TicketItem, TicketService, Picture
from django.forms.models import inlineformset_factory
from django.forms import modelformset_factory


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('birth_date', "email", "last_name", "first_name",)

class TicketCarForm(forms.ModelForm):

    class Meta:
        model = TicketCar
        exclude = ('seller', 'category', )

class TicketItemForm(forms.ModelForm):

    class Meta:
        model = TicketItem
        exclude = ('seller', 'category', )

class TicketServiceForm(forms.ModelForm):

    class Meta:
        model = TicketService
        exclude = ('seller', 'category', )


PictureFormSet = inlineformset_factory(
    TicketCar,
    Picture,
    fields=('image',),
    max_num=1
)

CarFormSet = modelformset_factory(
    TicketCar,
    fields=('name', 'text', 'model', 'year', 'color', 'price', 'tag',),
    max_num=1,
)