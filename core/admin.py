from django.contrib import admin

from .models import Master, Service, Order, Review
import datetime

# admin.site.register(Master)
# admin.site.register(Service)
# admin.site.register(Order)
admin.site.register(Review)

# Фильтр для OrderAdmin

class AppointmentDateFilter(admin.SimpleListFilter):
    title = 'Дата записи'
    parameter_name = 'appointment_date'

    def lookups(self, request, model_admin):
        return [
            ('today', 'Сегодня'),
            ('tomorrow', 'Завтра'),
            ('this_week', 'На этой неделе'),
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value == 'today':
            return queryset.filter(appointment_date__date=datetime.date.today())
        elif value == 'tomorrow':
            return queryset.filter(appointment_date__date=datetime.date.today() + datetime.timedelta(days=1))
        elif value == 'this_week':
            return queryset.filter(appointment_date__week=datetime.date.today().isocalendar()[1])
        



# Отображение полей
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client_name', 'phone', 'master', 'status', 'appointment_date', 'total_price']

# Поисковая форма
    search_fields = ['client_name', 'phone']

# Фильтрация
    list_filter = ['status', 'master', AppointmentDateFilter]

# Количество записей на странице
    # list_per_page = 10

# Кликабельные поля
    list_display_links = ['client_name', 'phone']

# редактирование поля
    list_editable = ['status']

# нередактируемые поля
    readonly_fields = ['date_created', 'date_updated', 'total_price']

#  кастомные действия
    actions = ['approve_status', 'cancel_status', 'complete_status', 'not_approved_status']

    @admin.action(description='Подтвердить заявку')
    def approve_status(self, request, queryset):
        queryset.update(status='approved')
    
    @admin.action(description='Отменить заявку')
    def cancel_status(self, request, queryset):
        queryset.update(status='canceled')

    @admin.action(description='Завершить заявку')
    def complete_status(self, request, queryset):
        queryset.update(status='completed')

    @admin.action(description='В работе')
    def not_approved_status(self, request, queryset):
        queryset.update(status='not_approved')

# кастомный столбец
    @admin.display(description='Общая стоимость')
    def total_price(self, obj):
        return sum(service.price for service in obj.services.all())
    
# Удобное отоброжение M2M услуг в детальном отображении
    filter_horizontal = ("services",)

# Группируем поля на странице редактирования
    fieldsets = (
        ("Основная информация", {"fields": ("client_name", "phone", "status", "comment")}),
        ("Детали записи", {"fields": ("master", "appointment_date", "services")}),
        (
            "Финансовая информация (только для чтения)",
            {
                "classes": ("collapse",),  # Делаем блок сворачиваемым
                "fields": ("total_price",),
            },
        ),
        (
            "Служебная информация (только для чтения)",
            {"classes": ("collapse",), "fields": ("date_created", "date_updated")},
        ),
    )

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'experience', 'is_active', 'count_services']


# Поисковая форма
    search_fields = ['name']

# Фильтрация
    list_filter = ['is_active', 'services']

# кастомный столбец
    @admin.display(description='Колличество услуг')
    def count_services(self, obj):
        return obj.services.count()


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration', 'is_popular']

# Поисковая форма
    search_fields = ['name']

# Фильтрация
    list_filter = ['is_popular']

