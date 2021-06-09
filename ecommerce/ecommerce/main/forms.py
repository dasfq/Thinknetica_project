from django import forms
from .models import Profile, TicketCar, TicketItem, TicketService

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