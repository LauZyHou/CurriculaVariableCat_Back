from rest_framework import serializers

from course.models import Course, SelectCourse
from users.models import UserProfile


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("id", "first_name")


class CourseDetailSerializer(serializers.ModelSerializer):
    """课程序列化"""

    teacher = TeacherSerializer()  # id转教师名

    class Meta:
        model = Course
        fields = "__all__"


class SelectCourseSerializer(serializers.ModelSerializer):
    """选课序列化"""

    class Meta:
        model = SelectCourse
        fields = "__all__"
