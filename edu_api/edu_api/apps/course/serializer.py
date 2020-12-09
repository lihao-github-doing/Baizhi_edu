from rest_framework.serializers import ModelSerializer

from course.models import CourseCategory, Course, Teacher, CourseLesson, CourseChapter


class CourseCategoryModelSerializer(ModelSerializer):
    """课程分类"""

    class Meta:
        model = CourseCategory
        fields = ("id", "name")


class TeacherModelSerializer(ModelSerializer):
    """讲师"""

    class Meta:
        model = Teacher
        fields = ("id", "name", "title", "signature", "image", "brief")


class CourseModelSerializer(ModelSerializer):
    """课程列表"""

    teacher = TeacherModelSerializer()

    class Meta:
        model = Course
        fields = ("id", "name", "course_img", "students", "lessons", "pub_lessons",
                  "price", "teacher", "lesson_list")

class CourseDetailModelSerializer(ModelSerializer):
    """课程详细信息的序列化器"""

    teacher = TeacherModelSerializer()

    class Meta:
        model = Course
        fields = ("id", "name", "course_img", "students", "lessons", "pub_lessons",
                  "price", "teacher", "level_name", "brief_html")


class CourseLessonModelSerializer(ModelSerializer):
    """课程课时信息"""

    class Meta:
        model = CourseLesson
        fields = ['id', "name", "free_trail", "duration"]


class CourseChapterModelSerializer(ModelSerializer):
    # 一堆多 需要指定参数 many=True
    coursesections = CourseLessonModelSerializer(many=True)

    class Meta:
        model = CourseChapter
        fields = ['id', 'chapter', 'name', "coursesections"]