from django.contrib import admin
from .models import Item, Purchase, Store

# Register your models here.
admin.site.register(Item)
admin.site.register(Purchase)
admin.site.register(Store)