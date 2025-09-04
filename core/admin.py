from django.contrib import admin

from .models import Master, Service, Order, Review

# admin.site.register(Master)
# admin.site.register(Service)
# admin.site.register(Order)
admin.site.register(Review)

# Отображение полей
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'phone', 'status', 'comment', 'master', 'date_created', 'date_updated']

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'address', 'experience', 'is_active']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']