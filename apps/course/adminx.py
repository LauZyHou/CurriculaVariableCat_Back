from course.models import Semester, Course, SelectCourse

import xadmin


class SemesterAdmin(object):
    """学期"""
    list_display = ["id", "year", "season"]


class CourseWeekAdmin(object):
    """上课星期"""
    list_display = ["id", "week"]


class CourseTimeAdmin(object):
    """上课时间"""
    list_display = ["id", "time"]


class CourseAdmin(object):
    """开课"""
    list_display = ["id", "teacher", "subject", "semester"]


class SelectCourseAdmin(object):
    """选课"""
    list_display = ["id", "student", "course"]


xadmin.site.register(Semester, SemesterAdmin)
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(SelectCourse, SelectCourseAdmin)
