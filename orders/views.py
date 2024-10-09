from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView
from common.views import TitleMixin
from products.models import Basket
from .forms import OrderForm
from .models import Order, OrderItem


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    title = 'Оформление заказа'

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        order = form.save()

        baskets = Basket.objects.filter(user=self.request.user)

        for basket in baskets:
            product = basket.product
            price = product.price
            quantity = basket.quantity
            OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)

        baskets.delete()

        return redirect("orders:success_create")


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Ваш заказ успешно сформирован'
