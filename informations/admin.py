from ckeditor.widgets import CKEditorWidget
from django.contrib import admin
from django.db import models

from informations.forms import DeliveryInformationForm, ReturnInformationForm
from informations.models import DeliveryInformation, ReturnInformation


@admin.register(DeliveryInformation)
class DeliveryInformationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    form = DeliveryInformationForm
    fields = ('name', 'text', 'price',)

    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }


@admin.register(ReturnInformation)
class ReturnInformationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    form = ReturnInformationForm
    fields = ('name', 'text',)

    formfield_overrides = {
        models.TextField: {'widget': CKEditorWidget}
    }
