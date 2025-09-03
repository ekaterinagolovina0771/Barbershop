from django.urls import reverse

def menu_items(request):
    """
    Контекстный процессор для добавления меню в контекст шаблонов.
    """
    menu = [
        {
            "name": "Главная", 
            "url_name": "landing" + "#top", 
            "url": reverse("landing")},
        {
            "name": "Мастера",
            "url": reverse("landing") + "#masters",
        },
        {
            "name": "Услуги",
            "url": reverse("landing") + "#services",
        },
        {
            "name": "Отзывы",
            "url": reverse("landing") + "#reviews",
        },
        {
            "name": "Записаться",
            "url": reverse("landing") + "#get-order",
        },
    ]

    staff_menu = [
        {
            "name": "Заявки",
            "url": reverse("orders"),
            "icon_class": "bi-clipboard-data",
        },
        {
            "name": "Список услуг",
            "url": reverse("services-list"),
            "icon_class": "bi-list-check",
        },
    ]

    return {"menu_items": menu, "menu_staff_items": staff_menu}
