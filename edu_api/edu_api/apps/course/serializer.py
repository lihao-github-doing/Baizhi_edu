from rest_framework.serializers import ModelSerializer

from course.models import CourseCategory, Course, Teacher, CourseLesson


class CourseCategoryModelSerializer(ModelSerializer):
    """课程分类"""

    class Meta:
        model = CourseCategory
        fields = ("id", "name")


class TeacherModelSerializer(ModelSerializer):
    """讲师"""

    class Meta:
        model = Teacher
        fields = ("id", "name", "title")


class CourseModelSerializer(ModelSerializer):
    """课程列表"""

    teacher = TeacherModelSerializer()

    class Meta:
        model = Course
        fields = ("id", "name", "course_img", "students", "lessons", "pub_lessons",
                  "price", "teacher", "lesson_list")


# class LessonsModelSerializer(ModelSerializer)
#     class Meta:
#         model = CourseLesson
#         fields = ("id",)