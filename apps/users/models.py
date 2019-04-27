from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    """用户(学生/教师).含管理员"""
    # 注意,字段学号/教师号即为username,在AbstractUser中
    # 字段名和姓氏也在AbstractUser中,考虑到方便只用first_name字段!
    KIND_CHOICES = (
        (True, "学生"),
        (False, "教师")
    )
    kind = models.BooleanField(choices=KIND_CHOICES, default=True, verbose_name="角色")
    head_img = models.ImageField(upload_to="user_head/", null=True, blank=True, verbose_name="用户头像")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = "用户们"

    def __str__(self):
        return self.username
