import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from django_redis import get_redis_connection

from course.models import Course
from edu_api.settings.constants import IMG_SRC
from course.models import CourseExpire

log = logging.getLogger('django')


class CartViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def add_cart(self, request):
        course_id = request.data.get('course_id')
        user_id = request.user.id
        # 勾选状态
        select = True
        # 有效期
        expire = 0

        # 校验前端传递的参数
        try:
            Course.objects.get(is_show=True, is_delete=False, id=course_id)
        except Course.DoesNotExist:
            return Response({"message": "您添加课程不存在"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            redis_connection = get_redis_connection("cart")
            pipeline = redis_connection.pipeline()
            pipeline.multi()
            pipeline.hset("cart_%s" % user_id, course_id, expire)
            pipeline.sadd("selected_%s" % user_id, course_id)
            pipeline.execute()
            course_len = redis_connection.hlen("cart_%s" % user_id)
        except:
            log.error("购物储存数据失败")
            return Response({"message": "参数有误,添加购物车失败"},
                            status=status.HTTP_507_INSUFFICIENT_STORAGE)

        return Response({"message": "添加课程成功", "cart_length": course_len},
                        status=status.HTTP_200_OK)

    def list_cart(self, request):
        """展示购物车"""
        user_id = request.user.id

        redis_connection = get_redis_connection("cart")
        cart_list_bytes = redis_connection.hgetall('cart_%s' % user_id)
        select_list_bytes = redis_connection.smembers('selected_%s' % user_id)
        data = []
        for course_id_byte, expire_id_byte in cart_list_bytes.items():
            course_id = int(course_id_byte)
            expire_id = int(expire_id_byte)

            try:
                course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
            except Course.DoesNotExist:
                continue
            data.append({
                "selected": True if course_id_byte in select_list_bytes else False,
                "course_img": IMG_SRC + course.course_img.url,
                "name": course.name,
                "id": course.id,
                "price": course.price,
                "expire_id": expire_id
            })
        return Response(data)
    def del_course(self, request, *args, **kwargs):
        """从购物车中删除某个课程"""
        user_id = request.user.id
        course_id = request.query_params.get('course_id')
        print(course_id)

        try:
            Course.objects.get(is_show=True, is_delete=False, pk=course_id)
        except Course.DoesNotExist:
            return Response({"message": "参数有误，当前商品已下架"}, status=status.HTTP_400_BAD_REQUEST)

        redis_connection = get_redis_connection('cart')
        pipe = redis_connection.pipeline()
        pipe.multi()
        pipe.hdel("cart_%s" % user_id, course_id)
        pipe.srem("select_%s" % user_id, course_id)
        pipe.execute()

        return Response({"message": "删除商品成功"})

    def change_select(self, request):
        """切换购物车商品的状态"""
        user_id = request.user.id
        selected = request.data.get("selected")
        course_id = request.data.get("course_id")
        try:
            Course.objects.get(is_show=True, is_delete=False, pk=course_id)
        except Course.DoesNotExist:
            return Response({"message": "参数有误！当前商品不存在"}, status=status.HTTP_400_BAD_REQUEST)

        redis_connection = get_redis_connection("cart")
        if selected:
            # 将商品添加至 set中  代表选中
            redis_connection.sadd("select_%s" % user_id, course_id)
        else:
            redis_connection.srem("select_%s" % user_id, course_id)

        return Response({"message": "状态切换成功~~~~~"})

    def change_expire(self, request):
        """改变redis的课程有效期"""
        user_id = request.user.id
        course_id = request.data.get("course_id")
        expire_id = request.data.get("expire_id")
        print(expire_id, "expire_id")

        try:
            course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)

            # 如果前端传递的有效期选项不是0  则修改对应的有效
            if expire_id > 0:
                expire_item = CourseExpire.objects.filter(is_delete=False, is_show=True, pk=expire_id)
                if not expire_item:
                    raise CourseExpire.DoesNotExist()
        except Course.DoesNotExist:
            return Response({"message": "操作的课程不存在"}, status=status.HTTP_400_BAD_REQUEST)

        redis_connection = get_redis_connection("cart")
        redis_connection.hset("cart_%s" % user_id, course_id, expire_id)

        # TODO  重新计算修改有效期的课程的价格
        real_price = course.real_expire_price(expire_id)

        return Response({"message": "切换有效期成功", "price": real_price})

    def get_select_course(self, request):
        """获取所有被选中的课程"""
        user_id = request.user.id
        redis_connection = get_redis_connection("cart")

        # 获取当前登录用户的购物车的所有商品
        cart_list = redis_connection.hgetall("cart_%s" % user_id)
        select_list = redis_connection.smembers("select_%s" % user_id)

        total_price = 0  # 已勾选的商品总价
        data = []

        for course_id_byte, expire_id_byte in cart_list.items():
            course_id = int(course_id_byte)
            expire_id = int(expire_id_byte)

            if course_id_byte in select_list:

                try:
                    # 获取购物车中所有的商品信息
                    course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
                except Course.DoesNotExist:
                    continue

                # 如果有效期的id大于0 则需要计算商品的价格 id不大于0则代表永久 需要默认值
                origin_price = course.price
                expire_text = "永久有效"

                if expire_id > 0:
                    try:
                        course_expire = CourseExpire.objects.get(pk=expire_id)

                        # 有效期对应的价格
                        origin_price = course_expire.price
                        expire_text = course_expire.expire_text

                    except CourseExpire.DoesNotExist:
                        pass

                # 根据已勾选的商品的对应有效期的价格计算最终勾选商品的价格
                real_expire_price = course.real_expire_price(expire_id)

                data.append({
                    'id': course.id,
                    # 'price': course.real_price(),
                    "course_img": IMG_SRC + course.course_img.url,
                    "name": course.name,
                    # 课程对应的有效期文本
                    "expire_text": expire_text,
                    # 获取有效期真实价格
                    "real_price": "%.2f" % float(real_expire_price),
                    # 原价
                    "price": origin_price,
                })

                # 商品所有的总价
                total_price += float(real_expire_price)

        total_price = "%.2f" % float(total_price)

        return Response({"course_list": data, "total_price": total_price, "message": "获取成功"})






