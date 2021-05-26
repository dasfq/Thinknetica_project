from django.contrib import admin
from django import forms
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget


class FlatPageAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())


class FlatPageAdmin(FlatPageAdmin):
    content = FlatPageAdminForm


    # fieldsets = (
    #     (None, {'fields': ('url', 'title', 'content', 'sites')}),
    #     (_('Advanced options'), {
    #         'classes': ('collapse',),
    #         'fields': (
    #             'enable_comments',
    #             'registration_required',
    #             'template_name',
    #         ),
    #     }),
    # )

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
