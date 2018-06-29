from django.shortcuts import render, HttpResponse
from django.views.generic import View

# 分页
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .forms import UserAskForm

from .models import CourseOrg, City

# Create your views here.
class OrgView(View):
    """
    课程机构列表
    """
    def get(self, request):
        all_orgs = CourseOrg.objects.all()

        #选出所有城市
        all_city = City.objects.all()

        # 根据点击量来获取热门机构
        hot_orgs = all_orgs.order_by("-click_nums")[:3]

        # 城市筛选
        city_id = request.GET.get("city", "")
        print(city_id)
        if city_id:
            all_orgs = all_orgs.filter(city_id = int(city_id))

        # 类别筛选
        category = request.GET.get('ct', "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == 'courses':
                all_orgs = all_orgs.order_by("-course_nums")

        #进行分页处理
        org_nums = all_orgs.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 3, request=request)
        orgs = p.page(page)
        return render(request, "org-list.html", {"all_orgs": orgs, "all_city": all_city, "org_nums":org_nums,
                                                 "city_id": city_id, "category": category, "hot_orgs":hot_orgs,
                                                 'sort': sort})


class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"您的字段有错误,请检查"}', content_type='application/json')


class OrgHomeView(View):
    """
   机构首页
    """
    def get(self, request, org_id):
        # 根据id取到课程机构
        # 向前端传值，表明现在在course页
        current_page = "home"
        course_org = CourseOrg.objects.get(id= int(org_id))
        course_org.click_nums += 1
        course_org.save()
        # 通过课程机构找到课程。内建的变量，找到指向这个字段的外键引用
        all_courses = course_org.course_set.all()[:4]
        all_teacher = course_org.teacher_set.all()[:2]
        # 向前端传值说明用户是否收藏
        has_fav = False
        # 必须是用户已登录我们才需要判断。
        # if request.user.is_authenticated():
        #     if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
        #         has_fav = True
        return render(request, 'org-detail-homepage.html',{
           'all_courses':all_courses,
            'all_teacher':all_teacher,
            'course_org': course_org,
            "has_fav": has_fav,
            "current_page":current_page,
        })


class OrgCourseView(View):
    """
   机构课程列表页
    """
    def get(self, request, org_id):
        # 根据id取到课程机构
        course_org = CourseOrg.objects.get(id= int(org_id))
        # 向前端传值，表明现在在course页
        current_page = "course"
        # 通过课程机构找到课程。内建的变量，找到指向这个字段的外键引用
        all_courses = course_org.course_set.all()
        return render(request, 'org-detail-course.html',{
           'all_courses':all_courses,
            'course_org': course_org,
            "current_page":current_page,
        })

class OrgTeacherView(View):
    """
   机构讲师列表页
    """
    def get(self, request, org_id):
        # 向前端传值，表明现在在home页
        current_page = "teacher"
        # 根据id取到课程机构
        course_org = CourseOrg.objects.get(id= int(org_id))
        # 通过课程机构找到课程。内建的变量，找到指向这个字段的外键引用
        all_teachers = course_org.teacher_set.all()
        # 向前端传值说明用户是否收藏
        return render(request, 'org-detail-teachers.html',{
           'all_teachers':all_teachers,
            'course_org': course_org,
            "current_page":current_page,
        })

class OrgDescView(View):
    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))

        return render(request, 'org-detail-desc.html', {'course_org': course_org, "current_page": current_page})