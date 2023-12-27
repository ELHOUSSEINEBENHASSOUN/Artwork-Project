from django.contrib import admin
from .models import *
from django.db.models import Model


# Register your models here.

def get_model_fields(model):
    fields = []
    for field in model._meta.fields:
        if isinstance(field, Model):
            continue
        fields.append(field.name)
    return fields


@admin.register(Profile)
class Profile(admin.ModelAdmin):
    list_display = get_model_fields(Profile)
    


@admin.register(Artwork)
class Artwork(admin.ModelAdmin):
    list_display = get_model_fields(Artwork)

@admin.register(DemandePret)
class DemandePret(admin.ModelAdmin):
    list_display = get_model_fields(DemandePret)
