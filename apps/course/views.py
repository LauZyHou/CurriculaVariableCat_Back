from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import authentication, permissions
from rest_framework.response import Response
from rest_framework import status

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
                          mixins.CreateModelMixin,
                          viewsets.GenericViewSet):
    """所选课程"""
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SelectCourseSerializer

    def get_queryset(self):
        """只允许读写自己选的课程"""
        return SelectCourse.objects.filter(student=self.request.user.id)

    def retrieve(self, request, *args, **kwargs):
        """获取指定所选课程(没用到)"""
        return super().retrieve(request, args, kwargs)

    def list(self, request, *args, **kwargs):
        """获取自己所选的全部课程(课表不用这个,见users的view)"""
        return super().list(request, args, kwargs)

    def destroy(self, request, *args, **kwargs):
        """退课"""
        print(request.data)
        return super().destroy(request, args, kwargs)

    def create(self, request, *args, **kwargs):
        """选课"""
        # 不管传的是谁的,换成当前用户的id
        use_dict = {'student': request.user.id, 'course': request.data['course']}
        """[1]不允许选多个同一门课"""
        # 注意!物理主键上联合unique在数据库级别实现了,也就是不允许一个学生选两次某课
        # 这里是业务级判断一下课程号有没有重复,也就是不允许一个学生选两门"数据结构"
        my_sub_logic_id = request.data['sub_logic_id']  # 前端顺便交过来避免多一次查库
        # 当前用户所选的所有课程(从选课表获得)
        myselectcourse = self.get_queryset()
        # 当前用户所选的所有课程,在开课表中的物理主键list
        mycourse_id_lst = [sc.course_id for sc in myselectcourse]
        # 当前用户所选的所有课程,在开课表中对应来的Course对象
        mycourse = Course.objects.filter(id__in=mycourse_id_lst)
        # 当前用户所选的所有课程,对应于学科表的"课程号"
        sub_id_lst = [c.sub_logic_id for c in mycourse]
        if my_sub_logic_id in sub_id_lst:  # 已经选过了
            return Response({'non_field_errors': ["你已经选过这类课了!要换老师/换时间就退了再选!"]}, status=status.HTTP_400_BAD_REQUEST)
        # print(use_dict)
        """[2]不允许时间冲突"""
        # 怎么计算?周一到周五0-4,一二节到十一十二十三0-5
        # 可以考虑:周一第一二节是0,三四节是1...周二第一二节是6
        # 所以只要判断周号*6+节号*3有没有重复,用set可以快速判断
        # 要考虑一件事,假如一个老师某课只有周三3-4节有,这课可以表示成:
        # week1=2,time1=1,week2=None,time2=None
        # 也可以表示成:
        # week2=2,time1=1,week2=2,time2=1
        # 如果数据库里没有对这东西做约束,那是允许出现第二种情况的!
        # 可以在数据库里约束一下,不过这里业务级别也要判断好!
        # 已选的课程的时间
        old_set = set([c.week1 * 6 + c.time1 for c in mycourse]) | set(
            [c.week2 * 6 + c.time2 for c in mycourse if c.week2 is not None and c.time2 is not None])
        # 当前要选的课程
        nowcourse = Course.objects.get(id=request.data['course'])
        # 两个时间值(val1不做判断相当于一个assert,数据库级别要保证开课时week1和time1都非空)
        val2 = None
        val1 = nowcourse.week1 * 6 + nowcourse.time1
        if nowcourse.week2 is not None and nowcourse.time2 is not None:
            val2 = nowcourse.week2 * 6 + nowcourse.time2
        # 判断时间冲突
        if val1 in old_set or (val2 is not None and val2 in old_set):
            return Response({'non_field_errors': ["和目前课表时间冲突!"]}, status=status.HTTP_400_BAD_REQUEST)
        """[3]做选课操作"""
        serializer = self.get_serializer(data=use_dict)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
