from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import authentication, permissions
from rest_framework.response import Response

from course.models import Course, SelectCourse
from course.serializers import CourseDetailSerializer, SelectCourseSerializer


class CourseViewSet(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """所开课程"""
    queryset = Course.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CourseDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        """获取指定sub_logic_id的课程(而不是course的物理主键id)"""
        res = Course.objects.filter(sub_logic_id=kwargs['pk'])
        serializer = self.get_serializer(res, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """获取课程列表"""
        # 模糊查询
        if 's' in request.query_params:
            mystr = request.query_params['s']
            queryset = Course.objects.filter(sub_name__contains=mystr)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        # 获取全部
        return super().list(request, args, kwargs)


class SelectCourseViewSet(mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    """所选课程"""
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SelectCourseSerializer

    def get_queryset(self):
        """只允许读写自己选的课程"""
        return SelectCourse.objects.filter(student=self.request.user.id)

    def retrieve(self, request, *args, **kwargs):
        """获取指定课程"""
        return super().retrieve(request, args, kwargs)

    def list(self, request, *args, **kwargs):
        """获取自己所选的全部课程"""
        return super().list(request, args, kwargs)

    def destroy(self, request, *args, **kwargs):
        """退课"""
        return super().destroy(request, args, kwargs)
