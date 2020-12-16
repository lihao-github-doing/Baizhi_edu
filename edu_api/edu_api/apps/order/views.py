from django.shortcuts import render

# Create your views here.
from rest_framework.generics import CreateAPIView

from order.models import Order
from order.serializer import OrderModelSerializer


class OrderAPIView(CreateAPIView):
    """订单详情"""
    queryset = Order.objects.filter(is_show=True, is_delete=False)
    serializer_class = OrderModelSerializer
