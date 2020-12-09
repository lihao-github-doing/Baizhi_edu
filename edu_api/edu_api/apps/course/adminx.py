import xadmin

from course.models import CourseCategory, Course, Teacher, CourseChapter, CourseLesson


class CourseCategoryAdmin(object):
    """课程分类表"""
    pass


xadmin.site.register(CourseCategory, CourseCategoryAdmin)


class CourseAdmin(object):
    """课程信息表"""
    pass


xadmin.site.register(Course, CourseAdmin)


class TeacherAdmin(object):
    """讲师表"""
    pass


xadmin.site.register(Teacher, TeacherAdmin)


class CourseChapterAdmin(object):
    """章节表"""
    pass


xadmin.site.register(CourseChapter, CourseChapterAdmin)


class CourseLessonAdmin(object):
    """课时表"""
    pass


xadmin.site.register(CourseLesson, CourseLessonAdmin)
