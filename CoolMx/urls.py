"""CoolMx URL Configuration

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
from django.views.generic import TemplateView
#from django.contrib import admin
from extra_apps import xadmin
from django.views.static import serve

from users.views import IndexView, LoginView, LogoutView,RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView
from organization.views import  OrgView
from CoolMx.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^captcha/', include('captcha.urls')),
    #url(r'^$', IndexView.as_view(), name="index"),
    url(r'^$', TemplateView.as_view(template_name="index.html"), name="index"),
    url('^login/$', LoginView.as_view(), name="login"),
    url('^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="active"),
    url(r'^forgetpwd/$', ForgetPwdView.as_view(), name="forgetpwd"),
    url(r'^forget/(?P<reset_code>.*)/$', ResetView.as_view(), name="reset"),
    url(r'^modify/$', ModifyPwdView.as_view(), name="modifypwd"),

    url(r'^org-list/$', OrgView.as_view(), name="org-list"),

    # 配置上传文件的访问处理
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT})
]
