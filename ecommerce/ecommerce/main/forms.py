from django import forms
from .models import Profile, TicketCar, TicketItem, TicketService, Picture
from django.forms.models import inlineformset_factory
from django.forms import modelformset_factory
from datetime import date

class ProfileForm(forms.ModelForm):

    def clean_birth_date(self):
        birth = self.cleaned_data['birth_date']
        today = date.today()
        if (birth.year + 18, birth.month, birth.day) > (today.year, today.month, today.day):
            raise forms.ValidationError('Must be at least 18 years old to register')
        return birth

    class Meta:
        model = Profile
        fields = ('birth_date', "email", "last_name", "first_name", "groups", 'group',)

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
    max_num=3
)