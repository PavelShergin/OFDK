from django.urls import path

from orders.views import OrderCreateView
from orders.views import SuccessTemplateView
from django.urls import path


app_name = 'orders'

urlpatterns = [
   path('order-create/', OrderCreateView.as_view(), name='order_create'),
   path('success-create/', SuccessTemplateView.as_view(), name='success_create'),

]
