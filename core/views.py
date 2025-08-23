# core/views.py
from django.shortcuts import render, HttpResponse
from .data import masters, services, orders

def landing(request) -> HttpResponse:
    '''
    Отвечает за маршрут '/'
    '''
    return render(request, "landing.html")
    
def thanks(request) -> HttpResponse:
    '''
    Отвечает за маршрут 'tanks/'
    '''
    return render(request, "thanks.html")

def orders_list(request) -> HttpResponse:
    '''
    Отвечает за маршрут 'orders/'
    '''
    context = {
        "orders": orders,
    }
    return render(request, "orders_list.html", context=context)

def order_detail(request, order_id) -> HttpResponse:
    '''
    Отвечает за маршрут 'orders/<int:order_id>/'
    param request: HttpRequest
    param order_id: id заявки
    '''
    order = [order for order in orders if order["id"] == order_id]
    try:
        order = order[0]
        context = {
            "order": order,
        }
    except IndexError:
        return HttpResponse("<h1>Заявка не найдена</h1>", status=404)

    rendom = 1
    return render(request, "order_detail.html", context=context)

