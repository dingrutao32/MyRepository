"""MxOline1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
import xadmin
#处理静态文件
from django.views.static import serve

from users.views import LoginView, RegisterView, ActiveUserVier, ForgetPwdView, ResetView, ModifyPwdView, LogoutView
from organization.views import OrgView
from users.views import IndexView
from MxOline1.settings import MEDIA_ROOT

urlpatterns = [
    url(r'admin', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url('^$', IndexView.as_view(), name="index"),
    #template_name="index.html"
    url('^login/$', LoginView.as_view(), name="login"),
    url('^logout/$', LogoutView.as_view(), name="logout"),
    url('^register/$', RegisterView.as_view(), name="register"),
    url(r'^captcha/', include('captcha.urls')),#注册验证码插件
    url(r'active/(?P<active_code>.*)/$',ActiveUserVier.as_view(), name="user_active"),
    url(r'^forget/$', ForgetPwdView.as_view(), name="forget_pwd"),
    url(r'reset/(?P<reset_code>.*)/$', ResetView.as_view(), name="reset_pwd"),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),

    #课程机构url配置
    url(r'^org/', include('organization.urls', namespace="org")),

    #课程相关url配置
    url(r'^course/', include('courses.urls', namespace="course")),

    #配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$', serve, {"document_root":MEDIA_ROOT}),

    #url(r'^static/(?P<path>.*)$', serve, {"document_root":STATIC_ROOT}),

    # 课程相关url配置
    url(r'^users/', include('users.urls', namespace="users")),

    # 富文本相关url
    url(r'^ueditor/',include('DjangoUeditor.urls' )),


]

#全局404页面配置
hander404 = 'user.views.page_not_found'
hander500 = 'user.views.page_error'