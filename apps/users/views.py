from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import authentication, permissions
from rest_framework.response import Response

from users.models import UserProfile
from course.models import SelectCourse


class KBViewSet(mixins.ListModelMixin,
                viewsets.GenericViewSet):
    """自己的课表"""
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = ''

    def list(self, request, *args, **kwargs):
        """获取自己的课表"""
        queryset = SelectCourse.objects.filter(student=request.user.id)
        ret_list = [{'xq1': None, 'xq2': None, 'xq3': None, 'xq4': None, 'xq5': None} for i in range(13)]  # 第一节课到第13节课
        for c in queryset:
            week1 = c.course.week1
            time1 = c.course.time1
            week2 = c.course.week2
            time2 = c.course.time2
            # 这里name用Subject的name(学科名),而id用SelectCourse的id(删课时候好删除)
            use_dict = {'name': c.course.subject.name, 'id': c.id}
            # use_dict = c.course.subject.name
            use_week1 = 'xq' + str(week1 + 1)
            use_week2 = 'xq' + str(week2 + 1)
            # 分别处理
            if week1 is not None:
                time1_a = time1 * 2
                ret_list[time1_a][use_week1] = use_dict
                if time1 == 5:
                    ret_list[11][use_week1] = use_dict
                    ret_list[12][use_week1] = use_dict
                else:
                    ret_list[time1_a + 1][use_week1] = use_dict
            print(ret_list)
            if week2 is not None:
                time2_a = time2 * 2
                ret_list[time2_a][use_week2] = use_dict
                if time2 == 5:
                    ret_list[11][use_week2] = use_dict
                    ret_list[12][use_week2] = use_dict
                else:
                    ret_list[time2_a + 1][use_week2] = use_dict
            print(ret_list)
        return Response(ret_list)
