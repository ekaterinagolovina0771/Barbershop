from django.urls import reverse

def menu_items(request):
    """
    Контекстный процессор для добавления меню в контекст шаблонов.
    """
    menu = [
        {"title": "Главная", "url_name": "landing", "url": reverse("landing")},
        {
            "title": "Мастера",
            "url": reverse("landing") + "#masters",
        },
        {
            "title": "Услуги",
            "url": reverse("landing") + "#services",
        },
        {
            "title": "Отзывы",
            "url": reverse("landing") + "#reviews",
        },
        {
            "title": "Записаться",
            "url": reverse("landing") + "#get-order",
        },
    ]

    menu_staff = [
        {"title": "Заявки", "url": reverse("orders")},
    ]

    return {"menu_items": menu, "menu_staff_items": menu_staff}
