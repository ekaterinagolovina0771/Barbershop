# core/views.py
from django.shortcuts import render, HttpResponse

def landing(request) -> HttpResponse:
    '''
    Отвечает за маршрут '/'
    '''
    return HttpResponse("<h1>Главная страница</h1>")

def thanks(request) -> HttpResponse:
    '''
    Отвечает за маршрут 'tanks/'
    '''
    return HttpResponse("<h1>Спасибо за заявку</h1>")

def orders_list(request) -> HttpResponse:
    '''
    Отвечает за маршрут 'orders/'
    '''
    return HttpResponse("<h1>Список заявок</h1>")

def order_detail(request, order_id) -> HttpResponse:
    '''
    Отвечает за маршрут 'orders/<int:order_id>/'
    param request: HttpRequest
    param order_id: id заявки
    '''
    return HttpResponse(f"<h1>Детали заявки {order_id}</h1>")

