from django.db import models

class Order(models.Model):
    STATUS_CHOICES = [
        ("not_approved", "Новая"),
        ("approved", "Подтверждена"),
        ("canceled", "Отменена"),
        ("completed", "Завершена"),
    ]
    client_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="not_approved", verbose_name='Статус')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    master = models.ForeignKey("Master", on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Мастер')
    services = models.ManyToManyField("Service", related_name='orders', verbose_name='Услуги')
    appointment_date = models.DateTimeField(verbose_name="Дата и время приема")

class Master(models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя")
    # photo = models.ImageField(_("Image"), upload_to="masters/", blank=True, verbose_name="Фотография")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    experience = models.PositiveIntegerField(verbose_name="Стаж работы", help_text="Опыт работы в годах")
    services = models.ManyToManyField("Service", related_name='masters', verbose_name='Услуги')
    is_active = models.BooleanField(default=True, verbose_name="Активен")
