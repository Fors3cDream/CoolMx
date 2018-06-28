from django.shortcuts import render
from django.views.generic import View

# 分页
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg, City

# Create your views here.
class OrgView(View):
    """
    课程机构列表
    """
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        all_city = City.objects.all()

        #进行分页处理
        org_nums = all_orgs.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 3, request=request)
        orgs = p.page(page)
        return render(request, "org-list.html", {"all_orgs": orgs, "all_city": all_city, "org_nums":org_nums})