from django.contrib import admin
from .models import Property

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'location', 'bedrooms', 'bathrooms', 'is_available')
    search_fields = ('title', 'location')
    list_filter = ('is_available', 'bedrooms', 'bathrooms')

