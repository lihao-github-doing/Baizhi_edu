import xadmin

from order.models import Order, OrderDetail


class OrderAdmin(object):
    """订单模型"""
    pass


xadmin.site.register(Order, OrderAdmin)


class OrderDetailAdmin(object):
    """订单详情"""
    pass


xadmin.site.register(OrderDetail, OrderDetailAdmin)
