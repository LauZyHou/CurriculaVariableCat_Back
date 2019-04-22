from django.db import models

from users.models import UserProfile
from subject.models import Subject


class Semester(models.Model):
    """学期"""
    SEASON_CHOICE = (
        ("spring", "春季学期"),
        ("summer", "夏季学期"),
        ("autumn", "秋季学期"),
        ("winter", "冬季学期")
    )
    year = models.CharField(max_length=4, verbose_name="学年", unique=True)
    season = models.CharField(max_length=6, choices=SEASON_CHOICE, verbose_name="季节")
    start_date = models.DateField(verbose_name="学期开始日期")
    end_date = models.DateField(verbose_name="学期结束日期")

    class Meta:
        verbose_name = "学期"
        verbose_name_plural = "学期们"
        unique_together = ("year", "season")

    def __str__(self):
        return self.year + self.season


class Course(models.Model):
    """开课"""
    teacher = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="开课教师")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="学科")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, verbose_name="学期")
    capacity = models.PositiveSmallIntegerField(verbose_name="课程容量")
    schedule = models.BinaryField(max_length=80, verbose_name="课程表")  # 5*13

    class Meta:
        verbose_name = "开课"
        verbose_name_plural = "开课们"

    def __str__(self):
        return self.subject.name + "({0},{1})".format(self.teacher.name, str(self.semester))


class SelectCourse(models.Model):
    """选课"""
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="选课学生")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")

    class Meta:
        verbose_name = "选课"
        verbose_name_plural = "选课们"
        unique_together = ("student", "course")

    def __str__(self):
        return self.student.name + "->" + str(self.course)
