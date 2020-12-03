from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    # 调用DRF自己的异常处理函数，返回响应
    response = exception_handler(exc, context)
    print(exc, context)
    if response is None:
        return Response({
            'detail': '%s,%s' % (context['view'], exc)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return response

