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

from utils.email_send import send_register_eamil

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
                if user.is_active:
                    login(request, user)
                    return render(request, "index.html")
                else:
                    return render(request, "login.html", {"msg":"用户未激活"})
            else:
                return render(request, "login.html", {"msg":"用户名或密码错误"})
        else:
            return render(request, "login.html", {"login_form":login_form})

class LogoutView(View):
    def get(self, request):
        # django自带的logout
        logout(request)
        # 重定向到首页,
        return HttpResponseRedirect(reverse("index"))


# 用户注册
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("user_name", "")
            if UserProfile.objects.filter(username=user_name):
                return render(request, "register.html", {'register_form':register_form, "msg":"用户名已存在"})
            email = request.POST.get("email", "")
            if UserProfile.objects.filter(email=email):
                return render(request, "register.html", {'register_form':register_form, "msg":"邮箱已注册"})
            pass_word =request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = email
            user_profile.password = make_password(pass_word)
            user_profile.is_active = False

            # 发送注册激活邮件
            if send_register_eamil(email, "register"):
                user_profile.save()
            else:
                return render(request, "register.html", {"msg": "发送激活邮件失败！请稍后再试！"})

            return render(request, "register.html", {"msg": "注册成功，请前往邮箱激活账号！"})
        else:
            return render(request, "register.html", {"register_form":register_form})

class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        return render(request, "login.html")

class ForgetPwdView(View):
    # get方法直接返回页面
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_form": forget_form})
        # post方法实现

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        # form验证合法情况下取出email
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            # 发送找回密码邮件
            send_register_eamil(email, "forget")
            # 发送完毕返回登录页面并显示发送邮件成功。
            return render(request, "login.html", {"msg": "重置密码邮件已发送,请注意查收"})
        # 如果表单验证失败也就是他验证码输错等。
        else:
            return render(
                request, "forgetpwd.html", {
                    "forget_from": forget_form})

# 重置密码的view


class ResetView(View):
    def get(self, request, reset_code):
        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_record:
            for record in all_record:
                # 获取到对应的邮箱
                email = record.email
                # 将email传回来
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(
                request, "forgetpwd.html", {"msg": "您的重置密码链接无效,请重新请求"})

class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            print(pwd1)
            pwd2 = request.POST.get("password2", "")
            print(pwd2)
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {'email':email, "msg":"两次密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, "login.html", {"msg":"密码修改成功，请登录"})
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modifypwd_form": modify_form})
