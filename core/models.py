from django.db import models

class Order(models.Model):
    '''
    Модель заявки
    Attributes:
        client_name (str): Имя клиента
        phone (str): Телефон
        comment (str): Комментарий
        status (str): Статус заявки
        date_created (datetime): Дата создания
        date_updated (datetime): Дата обновления
        master (Master): Мастер
        services (List[Service]): Список услуг
        appointment_date (datetime): Дата и время записи
 
    '''
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
    '''
    Модель мастера
    Attributes:
        name (str): Имя мастера
        photo (ImageField): Фотография мастера
        phone (str): Телефон мастера
        address (str): Адрес мастера
        experience (int): Опыт работы мастера
        services (List[Service]): Список услуг мастера
        is_active (bool): Активен ли мастер
    '''
    name = models.CharField(max_length=150, verbose_name="Имя")
    photo = models.ImageField(upload_to="masters/", blank=True, verbose_name="Фотография")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    experience = models.PositiveIntegerField(verbose_name="Стаж работы", help_text="Опыт работы в годах")
    services = models.ManyToManyField("Service", related_name='masters', verbose_name='Услуги')
    is_active = models.BooleanField(default=True, verbose_name="Активен")

class Service(models.Model):
    '''
    Модель услуги
    Attributes:
        name (str): Название услуги
        description (str): Описание услуги
        price (float): Цена услуги
        duration (int): Длительность услуги в минутах
        is_popular (bool): Популярная услуга
        image (ImageField): Изображение услуги
    '''
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    duration = models.PositiveIntegerField(verbose_name="Длительность", help_text="Время выполнения в минутах")
    is_popular = models.BooleanField(default=False, verbose_name="Популярная услуга")
    image = models.ImageField(upload_to="services/", blank=True, verbose_name="Изображение")

class Review(models.Model):
    '''
    Модель отзыва
    Attributes:
        text (str): Текст отзыва
        client_name (str): Имя клиента
        master (Master): Мастер
        photo (ImageField): Фотография
        created_at (datetime): Дата создания
        is_published (bool): Опубликован ли отзыв
    '''
    text = models.TextField(verbose_name="Текст отзыва")
    client_name = models.CharField(max_length=100, blank=True, verbose_name="Имя клиента")
    master = models.ForeignKey("Master", on_delete=models.CASCADE, verbose_name="Мастер")
    photo = models.ImageField(upload_to="reviews/", blank=True, null=True, verbose_name="Фотография")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    # rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="Оценка")
    is_published = models.BooleanField(default=True, verbose_name="Опубликован")

