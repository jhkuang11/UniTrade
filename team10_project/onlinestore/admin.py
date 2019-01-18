from django.contrib import admin
from .models import Item, Category

# admin.site.register(Item)
admin.site.register(Category)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_filter = ('approved',)
    pass
