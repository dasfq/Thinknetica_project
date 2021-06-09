from django import forms
from .models import Profile, TicketCar, TicketItem, TicketService

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('birth_date', "email", "last_name", "first_name",)

class TicketCarForm(forms.ModelForm):

    class Meta:
        model = TicketCar
        fields = ('name', 'text', 'seller',)

class TicketItemForm(forms.ModelForm):

    class Meta:
        model = TicketItem
        fields = ('name', 'text', 'seller',)


class TicketServiceForm(forms.ModelForm):

    class Meta:
        model = TicketService
        fields = ('name', 'text', 'seller',)
