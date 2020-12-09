# from django.shortcuts import render
#
# # Create your views here.
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.filters import OrderingFilter
# from rest_framework.generics import ListAPIView, RetrieveAPIView
#
# from course.models import CourseCategory, Course, CourseChapter
# from course.serializer import CourseCategoryModelSerializer, CourseModelSerializer, CourseDetailModelSerializer, \
#     CourseChapterModelSerializer
# from course.service import CoursePageNumberPagination
#
#
# class CourseCategoryAPIView(ListAPIView):
#     """课程分类查询"""
#     queryset = CourseCategory.objects.filter(is_show=True, is_delete=False).order_by("orders")
#     serializer_class = CourseCategoryModelSerializer
#
#
# class CourseAPIView(ListAPIView):
#     """课程列表"""
#     queryset = Course.objects.filter(is_show=True, is_delete=False).order_by("orders")
#     serializer_class = CourseModelSerializer
#
#     # 根据点击的分类的id不同来展示对应课程
#     filter_backends = [DjangoFilterBackend, OrderingFilter]
#     filter_fields = ("course_category",)
#
#     # 排序
#     ordering_fields = ("id", "students", "price")
#
#     # 分页的实现
#     pagination_class = CoursePageNumberPagination
#
# class CourseDetailAPIView(RetrieveAPIView):
#     """查询单个课程的信息"""
#     queryset = Course.objects.filter(is_delete=False, is_show=True)
#     serializer_class = CourseDetailModelSerializer
#
#
# class CourseLessonAPIView(ListAPIView):
#     """课程章节  课程章节对应课时"""
#     queryset = CourseChapter.objects.filter(is_show=True, is_delete=False).order_by("orders")
#     serializer_class = CourseChapterModelSerializer
#     filter_backends = [DjangoFilterBackend]
#     filter_fields = ['course']
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView

from course.models import CourseCategory, Course, CourseChapter
from course.serializer import CourseCategoryModelSerializer, CourseModelSerializer, CourseDetailModelSerializer, \
    CourseChapterModelSerializer
from course.service import CoursePageNumberPagination


class CourseCategoryAPIView(ListAPIView):
    """课程分类查询"""
    queryset = CourseCategory.objects.filter(is_show=True, is_delete=False).order_by("orders")
    serializer_class = CourseCategoryModelSerializer


class CourseAPIView(ListAPIView):
    """课程列表"""
    queryset = Course.objects.filter(is_show=True, is_delete=False).order_by("orders")
    serializer_class = CourseModelSerializer

    # 根据点击的分类的id不同来展示对应课程
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ("course_category",)

    # 排序
    ordering_fields = ("id", "students", "price")

    # 分页的实现
    pagination_class = CoursePageNumberPagination


class CourseDetailAPIView(RetrieveAPIView):
    """查询单个课程的信息"""
    queryset = Course.objects.filter(is_delete=False, is_show=True)
    serializer_class = CourseDetailModelSerializer


class CourseLessonAPIView(ListAPIView):
    """课程章节  课程章节对应课时"""
    queryset = CourseChapter.objects.filter(is_show=True, is_delete=False).order_by("orders")
    serializer_class = CourseChapterModelSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['course']
