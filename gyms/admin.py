from django.contrib import admin
from .models import Gym


@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'rating', 'monthly_fee', 'is_active')
    list_filter = ('state', 'city', 'is_active')
    search_fields = ('name', 'city', 'state', 'pincode')
    prepopulated_fields = {'slug': ('name',)}
