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
    TIME_CHOICE = (
        (0, "1-2"),
        (1, "3-4"),
        (2, "5-6"),
        (3, "7-8"),
        (4, "9-10"),
        (5, "11-13")
    )
    WEEK_CHOICE = (
        (0, "星期一"),
        (1, "星期二"),
        (2, "星期三"),
        (3, "星期四"),
        (4, "星期五")
    )
    teacher = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="开课教师")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="学科")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, verbose_name="学期")
    capacity = models.PositiveSmallIntegerField(verbose_name="课程容量")
    week1 = models.PositiveSmallIntegerField(choices=WEEK_CHOICE, verbose_name="上课周(其一)",
                                             null=True, blank=True)
    time1 = models.PositiveSmallIntegerField(choices=TIME_CHOICE, verbose_name="上课时间(其一)",
                                             null=True, blank=True)
    week2 = models.PositiveSmallIntegerField(choices=WEEK_CHOICE, verbose_name="上课周(其二)",
                                             null=True, blank=True)
    time2 = models.PositiveSmallIntegerField(choices=TIME_CHOICE, verbose_name="上课时间(其二)",
                                             null=True, blank=True)

    class Meta:
        verbose_name = "开课"
        verbose_name_plural = "开课们"

    def __str__(self):
        return self.subject.name + "({0},{1})".format(self.teacher.first_name, str(self.semester))


class SelectCourse(models.Model):
    """选课"""
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="选课学生")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")

    class Meta:
        verbose_name = "选课"
        verbose_name_plural = "选课们"
        unique_together = ("student", "course")

    def __str__(self):
        return self.student.first_name + "->" + str(self.course)
