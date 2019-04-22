from datetime import datetime

from django.db import models


class Subject(models.Model):
    """课程"""
    CATEGORY_CHOICE = (
        ("JC", "基础课"),
        ("BX", "必修课"),
        ("TX", "通选课"),
        ("ZX", "专业选修课"),
        ("XY", "新生研讨课")
    )
    name = models.CharField(max_length=20, verbose_name="课程名")
    logic_id = models.CharField(max_length=8, verbose_name="课程号", unique=True)
    category = models.CharField(choices=CATEGORY_CHOICE, max_length=2, verbose_name="种类")
    credit = models.PositiveSmallIntegerField(verbose_name="学分")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = "课程们"

    def __str__(self):
        return self.name
