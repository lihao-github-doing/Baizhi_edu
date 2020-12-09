import random

from django_redis import get_redis_connection
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status as http_status
from rest_framework.viewsets import ModelViewSet

from edu_api.settings import constants

from edu_api.libs.geetest import GeetestLib
from edu_api.utils.send_msg import Message
from user.models import UserInfo
from user.serializer import UserModelSerializer
from user.service import get_user_by_account

pc_geetest_id = "759d5436a6bfe1e0a94d222e9452097b"
pc_geetest_key = "2061a99f3c25e50989a0c04536132953"


class CaptchaAPIView(APIView):
    """极验验证码"""

    user_id = 1
    status = False

    def get(self, request):
        """获取验证码"""
        username = request.query_params.get("username")
        user = get_user_by_account(username)
        print(username)
        print(user)
        if user is None:
            return Response({"message": "该用户不存在"},
                            status=http_status.HTTP_400_BAD_REQUEST)

        self.user_id = user.id

        # 通过极验类生成验证码对象
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        print(gt)
        self.status = gt.pre_process(self.user_id)
        response_str = gt.get_response_str()
        print(response_str)
        return Response(response_str)

    def post(self, request):
        """验证验证码"""

        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.data.get("geetest_challenge")
        validate = request.data.get("geetest_validate")
        seccode = request.data.get("geetest_seccode")
        # 判断用户是否存在
        if self.user_id:
            result = gt.success_validate(challenge, validate, seccode, self.user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        print(result)
        result = {"status": "success"} if result else {"status": "fail"}
        return Response(result)
# class GetUserAPIView(APIView):
#     def get(self,request,*args,**kwargs):
#         username = request.query_params.filter('username')
#         print(username)
#         return Response(username)
class UserAPIView(CreateAPIView):
    """用户注册"""
    queryset = UserInfo.objects.all()
    serializer_class = UserModelSerializer


class SendMessageAPIView(APIView):

    def get(self, request, *args, **kwargs):
        """
        获取验证码  为手机号生成验证码并发送
        :param request:
        :return:
        """
        # 获取redis连接
        redis_connection = get_redis_connection("sms_code")

        # TODO 1. 判断手机号在60s内是否发送过短信
        phone = request.query_params.get("phone")
        phone_code = redis_connection.get("sms_%s" % phone)
        if phone_code is not None:
            return Response({"message": "您已经在60s内发送过短信了~"}, status=http_status.HTTP_400_BAD_REQUEST)

        # TODO 2. 生成随机的短信验证码
        code = random.randint(100000, 999999)
        print(code)
        # TODO 3. 将验证码保存至redis
        redis_connection.setex("sms_%s" % phone, constants.SMS_EXPIRE_TIME, code)
        redis_connection.setex("mobile_%s" % phone, constants.PHONE_EXPIRE_TIME, code)

        # TODO 4. 调用方法  完成短信的发送
        try:
            msg = Message(constants.API_KEY)
            msg.send_message(phone, code)
        except:
            return Response({"message": "短信发送失败"}, status=http_status.HTTP_500_INTERNAL_SERVER_ERROR)

        # TODO 5. 将发送的结果响应回去
        return Response({"message": "短信发送成功"}, status=http_status.HTTP_200_OK)

#
# class SendCodeAPIView(APIView):
#     def get (self,request,*args,**kwargs):
#         numbers = request.query_params.get('numbers')
#         redis_connection = get_redis_connection("sms_numbers")
#         if numbers != redis_connection:
#             return Response({"message":"验证失败"},status=http_status.HTTP_400_BAD_REQUEST)
#         return Response({"message":"验证成功"},status=http_status.HTTP_200_OK)

class PhoneAPIView(ModelViewSet):
    """手机号唯一验证"""

    def phone(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        print(phone)
        phonee = UserInfo.objects.filter(phone=phone)
        if phonee:
            return Response({
                'message': '手机号已存在',
            }, status=http_status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'message': 'ok',
            }, status=http_status.HTTP_200_OK)

class Phonee(ModelViewSet):
    """手机号验证"""

    def phone(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        print(phone)
        phonee = UserInfo.objects.filter(phone=phone)
        if phonee:
            return Response({
                'message': 'ok',
            }, status=http_status.HTTP_200_OK)
        else:
            return Response({
                'message': '手机号不存在',
            }, status=http_status.HTTP_400_BAD_REQUEST)