from datetime import datetime
from django.db import models

from users.models import UserProfile
from courses.models import Course

# Create your models here.
#用户咨询表单
class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name="姓名")
    mobile = models.CharField(max_length=11, verbose_name="手机")
    course_name = models.CharField(max_length=50, verbose_name="课程名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户咨询"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户: {0} 手机号: {1}'.format(self.name, self.mobile)


# 用户评论表单
class CourseComments(models.Model):

    course = models.ForeignKey(Course, verbose_name="课程")
    user = models.ForeignKey(UserProfile, verbose_name="用户")
    comments = models.CharField(max_length=250, verbose_name="评论")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="评论时间")

    class Meta:
        verbose_name = "用户评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '用户({0} 对于 《{1}》的评论 :'.format(self.user, self.course)


# 对于课程 机构 讲师的收藏
class UserFavorite(models.Model):
    TYPE_CHOICES = (
        (1, '课程'),
        (2, '课程机构'),
        (3, '讲师')
    )

    user = models.ForeignKey(UserProfile, verbose_name='用户')

    fav_id = models.IntegerField(default=0)
    fav_type = models.IntegerField(choices=TYPE_CHOICES, default=1, verbose_name='收藏类型')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}收藏了{1}'.format(self.user, self.fav_type)


# 用户消息表
class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name="接收用户id")
    message = models.CharField(max_length=500, verbose_name="消息内容")

    has_read = models.BooleanField(default=False, verbose_name="是否已读")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="发送时间")

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "向用户{0}发送了消息".format(self.user)


# 用户的课程表
class UserCourse(models.Model):
    course = models.ForeignKey(Course, verbose_name="课程")
    user = models.ForeignKey(UserProfile, verbose_name="用户")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "用户({0})的课程《{1}》".format(self.user, self.course)