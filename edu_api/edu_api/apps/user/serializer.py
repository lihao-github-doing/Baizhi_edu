import re

from django.contrib.auth.hashers import make_password
from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from user import views
from user.models import UserInfo
from user.service import get_user_by_account



class UserModelSerializer(ModelSerializer):
    """
    1. 对前端发送的参数进行安全校验
    2. 对相关字段进行处理  用户名  密码加密  邮箱
    3. 为注册成功的用户生成token
    """

    token = serializers.CharField(max_length=1024, read_only=True, help_text="用户token")
    sms_code = serializers.CharField(max_length=1024, write_only=True)

    class Meta:
        model = UserInfo
        fields = ("phone", "password", "id", "username", "token", "sms_code")

        extra_kwargs = {
            "phone": {
                "write_only": True
            },
            "password": {
                "write_only": True
            },
            "id": {
                "read_only": True
            },
            "username": {
                "read_only": True
            },
        }

    def validate(self, attrs):
        # """前端参数校验"""
        # phone = attrs.get("phone")
        # password = attrs.get("password")
        # # 获取用户输入的验证码
        # sms_code = attrs.get("sms_code")
        #
        # # 验证手机号
        # if not re.match(r'^1[3-9]\d{9}$', phone):
        #     raise serializers.ValidationError("手机号不符合格式")
        #
        # # TODO 1. 验证密码  最少8位 两到三种字符
        # if len(password) <= 11:
        #     raise serializers.ValidationError("密码不符合格式")
        # # 验证手机号是否已存在
        # try:
        #     user = get_user_by_account(phone)
        # except UserInfo.DoesNotExist:
        #     user = None
        #
        # if user:
        #     raise serializers.ValidationError("手机号已注册")
        #
        # # TODO 2. 验证手机号对应的验证码是否正确
        # # 限制总共可以验证多少次 3次
        # sums = 0
        # code = views.SendMessageAPIView.get().code
        # if sms_code ==code:
        #     print(sms_code)
        # elif sms_code !=code:
        #     sums += 1
        #     if sums >= 3:
        #         raise serializers.ValidationError("不能超过三次")
        #
        # # 成功验证码后需要及时删除验证码
        #
        # return attrs
        """前端参数校验"""
        phone = attrs.get('phone')
        password = attrs.get('password')
        sms_code = attrs.get('sms_code')
        print(phone, password, sms_code)
        # 验证验证码
        redis_connection = get_redis_connection('sms_code')
        phone_code = redis_connection.get('mobile_%s' % phone)
        print(phone_code)
        if phone_code.decode('utf-8') != sms_code:
            raise serializers.ValidationError('验证码错误')
        # 验证手机号
        if not re.match(r'^1[3-9]\d{9}$', phone):
            raise serializers.ValidationError('手机号格式不正确')
        # 验证密码
        if not re.match(r'^(?![\d]+$)(?![a-zA-Z]+$)(?![^\da-zA-Z]+$).{6,18}$', password):
            raise serializers.ValidationError('密码格式为6-18位，数字/字母/特殊字符任意两种组合')
        # 验证手机号是否已存在
        try:
            user = get_user_by_account(phone)
        except UserInfo.DoesNotExist:
            user = None
        if user:
            return serializers.ValidationError('手机号已被注册')
        # TODO 2. 验证手机号对应的验证码是否正确
        # 限制总共可以验证多少次 3次

        # 成功验证码后需要及时删除验证码
        return attrs

    def create(self, validated_data):
        """用户信息设置"""
        # 获取密码  对密码进行加密
        password = validated_data.get("password")
        hash_pwd = make_password(password)
        print(hash_pwd)

        # 处理用户名  设置默认值  随机生成字符串  手机号
        phone = validated_data.get("phone")

        # 为用户添加数据
        user = UserInfo.objects.create(
            phone=phone,
            username=phone,
            password=hash_pwd
        )

        # 为注册成功的用户生成token  完成自动登录
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        user.token = jwt_encode_handler(payload)

        return user
