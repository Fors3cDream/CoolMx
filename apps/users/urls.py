_author_ = "killer"
_date_ = "6/29/18 11:08 AM"

from django.conf.urls import url
from .views import UserInfoView, UploadImageView, UpdatePwdView

urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name="user-info"),

    url(r'image/upload/$', UploadImageView.as_view(), name="image-upload"),
    url(r'updatepwd/$', UpdatePwdView.as_view(), name='updatepwd'),
    ]