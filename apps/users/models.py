from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    """用户(学生/教师).含管理员"""
    KIND_CHOICES = (
        (True, "学生"),
        (False, "教师")
    )
    name = models.CharField(max_length=10, verbose_name="姓名")
    logic_id = models.CharField(max_length=9, verbose_name="学号/教师号", unique=True)
    kind = models.BooleanField(choices=KIND_CHOICES, default=True, verbose_name="角色")
    head_img = models.ImageField(upload_to="user_head/", null=True, blank=True, verbose_name="用户头像")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户们"

    def __str__(self):
        return self.name
