# core/views.py
from django.shortcuts import render, HttpResponse
# from .data import orders
from .models import Master, Service, Order, Review
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg


def landing(request) -> HttpResponse:
    """
    Отвечает за маршрут '/'
    """
    masters = Master.objects.all()
    services = Service.objects.all()
    reviews = Review.objects.all()  

    context = {
        "masters": masters,
        "services": services,
        "reviews": reviews,
    }
    return render(request, "landing.html", context=context)

    
def thanks(request) -> HttpResponse:
    '''
    Отвечает за маршрут 'tanks/'
    '''
    return render(request, "thanks.html")

@login_required
def orders_list(request) -> HttpResponse:
    '''
    Отвечает за маршрут 'orders/'
    '''
   # Получаю из GET запроса все данные URL
    # ПОИСКОВАЯ ФОРМА
    search_query = request.GET.get("q", "")
    # ЧЕКБОКСЫ выборки по полям
    # 1. поиск по телефону - search_by_phone
    # 2. поиск по имени - search_by_client_name
    # 3. поиск по тексту комментария - search_by_comment
    checkbox_client_name = request.GET.getlist("search_by_client_name", "")
    checkbox_phone = request.GET.getlist("search_by_phone", "")
    checkbox_comment = request.GET.getlist("search_by_comment", "")
    # ЧЕКББОКСЫ выборки по статусам
    # status_not_approved
    # status_approved
    # status_completed
    # status_canceled
    checkbox_status_not_approved = request.GET.get("status_not_approved", "")
    checkbox_status_approved = request.GET.get("status_approved", "")
    checkbox_status_completed = request.GET.get("status_completed", "")
    checkbox_status_canceled = request.GET.get("status_canceled", "")

    # РАДИОКНОПКА Порядок сортировки по дате
    # order_by_date - desc, asc
    order_by_date = request.GET.get("order_by_date", "desc")

    # 1. Создаем Q-объект для текстового поиска
    search_q = Q()
    if search_query:
        if checkbox_phone == "on":
            search_q |= Q(phone__icontains  =search_query)
        if checkbox_client_name == "on":
            search_q |= Q(client_name__lower__contains=search_query.lower())
        if checkbox_comment == "on":
            search_q |= Q(comment__icontains=search_query)

    # 2. Создаем Q-объект для фильтрации по статусам
    status_q = Q()
    # Условия статусов тоже объединяем через ИЛИ (|=)
    if checkbox_status_not_approved:
        status_q |= Q(status="not_approved")
    if checkbox_status_approved:
        status_q |= Q(status="approved")
    if checkbox_status_completed:
        status_q |= Q(status="completed")
    if checkbox_status_canceled:
        status_q |= Q(status="canceled")

    # Порядок сортировки
    ordering = "-date_created" if order_by_date == "desc" else "date_created"

    # 3. Объединяем два Q-объекта через И (&)
    # Это гарантирует, что запись должна соответствовать И условиям поиска, И условиям статуса
    orders = Order.objects.prefetch_related("services").select_related("master").filter(search_q & status_q).order_by(ordering)

    context = {"orders": orders}
    for order in orders:
        order.services_list = order.services.all()
        
    return render(request, "orders_list.html", context=context)

@login_required
def order_detail(request, order_id) -> HttpResponse:
    '''
    Отвечает за маршрут 'orders/<int:order_id>/'
    param request: HttpRequest
    param order_id: id заявки
    '''
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return HttpResponse('Заявка не найдена')
    order.services_list = order.services.all()
    context = {'order': order}
    return render(request, "order_detail.html", context)

def master_list(request):
    masters = Master.objects.annotate(rating=Avg('reviews__rating')).values('name', 'rating')
    print(masters)
    return render(request, 'landing.html', {'masters': masters})