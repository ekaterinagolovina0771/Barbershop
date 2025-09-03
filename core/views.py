# core/views.py
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Master, Service, Order, Review
from django.db.models import Q, Avg, Sum, Count
from django.contrib.auth.decorators import login_required
from .forms import OrderForm



def landing(request) -> HttpResponse:
    """
    Отвечает за маршрут '/'
    """
    masters = Master.objects.prefetch_related('services').annotate(num_services=Count('services'))
    services = Service.objects.all()
    reviews = Review.objects.select_related('master').all()  

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
    checkbox_client_name = request.GET.get("search_by_client_name", "")
    checkbox_phone = request.GET.get("search_by_phone", "")
    checkbox_comment = request.GET.get("search_by_comment", "")
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
        if checkbox_phone:
            search_q |= Q(phone__icontains=search_query)
        if checkbox_client_name:
            search_q |= Q(client_name__lower__icontains=search_query.lower())
        if checkbox_comment:
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

    return render(request, "orders_list.html", context=context)

@login_required
def order_detail(request, order_id) -> HttpResponse:
    '''
    Отвечает за маршрут 'orders/<int:order_id>/'
    param request: HttpRequest
    param order_id: id заявки
    '''
    try:
        order = Order.objects.prefetch_related("services").select_related("master").annotate(total_price=Sum('services__price')).get(id=order_id)
    except Order.DoesNotExist:
        return HttpResponse('Заявка не найдена')
    context = {'order': order}
    return render(request, "order_detail.html", context)

def master_list(request):
    masters = Master.objects.annotate(rating=Avg('reviews__rating')).values('name', 'rating')
    print(masters)
    return render(request, 'landing.html', {'masters': masters})

def order_page(request):
    form = OrderForm()
    return render(request, 'order_page.html', {'form': form})

def order_create(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Заявка успешно отправлена!")
            return redirect("thanks")
        # Если форма невалидна, снова рендерим страницу с формой и ошибками
        return render(request, 'order_page.html', {'form': form})
    # Если метод не POST, перенаправляем на страницу с формой
    return redirect('order-page')


def services_list(request):
    services = Service.objects.all()
    return render(request, "services_list.html", {"services": services})
