from django.contrib import admin
from django.db import models
from django import forms
from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin
from ckeditor.widgets import CKEditorWidget
from .models import Category, CustomUser, Seller, Tag, TicketCar, TicketItem, TicketService,\
    TicketServiceArchive, TicketCarArchive, TicketItemArchive


class FlatPageAdmin(FlatPageAdmin):
    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

class CustomUserAdmin(admin.ModelAdmin):
    pass

class SellerAdmin(admin.ModelAdmin):
    list_display = ('user','tickets_number',)

    def tickets_number(self, obj):
        return obj.ticket_qty

    tickets_number.short_description = 'Кол-во объявлений'

class TagAdmin(admin.ModelAdmin):
    pass

class TicketAdmin(admin.ModelAdmin):
    list_display = ('date_modified', 'name', 'seller', 'price',)
    ordering = ('date_modified',)

class TicketCarAdmin(TicketAdmin):
    pass

class TicketServiceAdmin(TicketAdmin):
    pass

class TicketItemAdmin(TicketAdmin):
    pass

class TicketServiceArchiveAdmin(TicketAdmin):
    pass

class TicketCarArchiveAdmin(TicketAdmin):
    pass

class TicketItemArchiveAdmin(TicketAdmin):
    pass

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Seller, SellerAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(TicketCar, TicketCarAdmin)
admin.site.register(TicketItem, TicketItemAdmin)
admin.site.register(TicketService, TicketServiceAdmin)
admin.site.register(TicketCarArchive, TicketCarArchiveAdmin)
admin.site.register(TicketItemArchive, TicketItemArchiveAdmin)
admin.site.register(TicketServiceArchive, TicketServiceArchiveAdmin)

