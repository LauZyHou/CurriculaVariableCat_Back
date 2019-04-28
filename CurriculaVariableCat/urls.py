"""CurriculaVariableCat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.views.static import serve
from django.urls import path, re_path, include
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken import views

import xadmin
from xadmin.plugins import xversion
from CurriculaVariableCat.settings import MEDIA_ROOT

xadmin.autodiscover()
from xadmin.plugins import xversion

xversion.register_models()

from users.views import KBViewSet
from course.views import CourseViewSet, SelectCourseViewSet

# DRF:REST风格的router
router = DefaultRouter()
router.register(r'kb', KBViewSet, base_name='kb')
router.register(r'course', CourseViewSet, base_name='course')
router.register(r'selectcourse', SelectCourseViewSet, base_name='selectcourse')

urlpatterns = [
    path('', include(router.urls)),
    path('xadmin/', xadmin.site.urls),
    # 处理图片显示的url,使用Django自带serve,传入参数告诉它去哪个路径找,使用配置好的路径
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
    # 自动化文档,1.11版本中注意此处前往不要加$符号
    path('docs/', include_docs_urls(title="CET6Cat文档")),
    # DRF调试登录,配置了这个API ROOT的调试才会有登录按钮
    path('api-auth/', include('rest_framework.urls')),
    # jwt的token认证,现在改用这个而不用上面那个drf自带的了
    path('login/', obtain_jwt_token),
]
