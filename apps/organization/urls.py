_author_ = "killer"
_date_ = "6/29/18 11:02 AM"
from django.conf.urls import url
from .views import  OrgView, AddUserAskView, OrgHomeView, \
                    OrgDescView, OrgTeacherView, OrgCourseView, \
                    AddFavView, TeacherListView, TeacherDetailView

urlpatterns = [
    url(r'^list/$', OrgView.as_view(), name="org-list"),
    url(r'^add_ask/$', AddUserAskView.as_view(), name="add-ask"),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="org-home"),
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name="org-course"),
    url(r'^org-teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name="org-teacher"),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name="org-desc"),

    # 机构搜藏
    url(r'^add_fav/$', AddFavView.as_view(), name="add-fav"),

    # 讲师列表
    url(r'^teachers/list/$', TeacherListView.as_view(), name="teachers-list"),
    # 访问机构讲师
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="teacher-detail"),
    ]