from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse

# Django自带的用户验证,login
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend

# 基于类实现需要继承的view
from django.views.generic.base import View
# form表单验证 & 验证码
from .forms import LoginForm, RegisterForm, ActiveForm, ForgetForm, ModifyPwdForm
# 进行密码加密
from django.contrib.auth.hashers import make_password
# 并集运算
from django.db.models import Q

from .models import Banner, UserProfile, EmailVerifyRecord
from courses.models import Course
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher

# Create your views here.

# 实现用户名邮箱均可登录
# 继承ModelBackend类，重写authenticate
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询
            user = UserProfile.objects.get(
                Q(username=username) | Q(email=username))
            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self,
            # raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None

# 首页
class IndexView(View):
    def get(self,request):
        # 取出轮播图
        all_banner = Banner.objects.all().order_by('index')[:5]
        # 正常位课程
        courses = Course.objects.filter(is_banner=False)[:6]
        # 轮播图课程取三个
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        # 课程机构
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {
            "all_banner":all_banner,
            "courses":courses,
            "banner_courses":banner_courses,
            "course_orgs":course_orgs,
        })

# 登录
class LoginView(View):
    # 直接调用 get 方法
    def get(self, request):
        redirect_url = request.GET.get('next', '')
        return render(request, "login.html", {"redirect_url": redirect_url})

    def post(self, request):
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")

            user = authenticate(username = user_name, password = pass_word)

            if user:
                login(request, user)
                return render(request, "index.html")
            else:
                return render(request, "login.html", {"msg":"用户名或密码错误"})
        else:
            return render(request, "login.html", {"login_form":login_form})


# 激活用户的view
class ActiveUserView(View):
    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        # 如果不为空也就是有用户
        active_form = ActiveForm(request.GET)
        if all_record:
            for record in all_record:
                # 获取到对应的邮箱
                email = record.email
                # 查找到邮箱对应的user
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                # 激活成功跳转到登录页面
                return render(request, "login.html", )
        # 自己瞎输的验证码
        else:
            return render(
                request, "register.html", {
                    "msg": "您的激活链接无效", "active_form": active_form})