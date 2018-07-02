_author_ = "killer"
_date_ = "7/2/18 2:02 PM"

from django.conf.urls import url

from .views import CourseListView, CourseDetailView, CourseInfoView

urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name="course-list"),

    # 课程详情页
    url(r'^course/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course-detail"),
# 课程章节信息页
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name="course-info"),
    ]