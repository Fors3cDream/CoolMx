from datetime import datetime

from django.db import models

from organization.models import CourseOrg, Teacher

#课程信息表
class Course(models.Model):
    DEGREE_CHOICES = (
        ('cj', "初级"),
        ('zj', "中极"),
        ('gj', "高级")
    )

    course_org = models.ForeignKey(CourseOrg, verbose_name="所属机构", null=True, blank=True)
    teacher = models.ForeignKey(Teacher, verbose_name="讲师", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name="课程名称")
    desc = models.CharField(max_length=300, verbose_name="课程描述")
    detail = models.TextField(verbose_name="详细信息")
    is_banner = models.BooleanField(default=False, verbose_name="是否轮播")
    degree = models.CharField(choices=DEGREE_CHOICES, verbose_name="难度", max_length=2)
    learn_times = models.IntegerField(default=0, verbose_name="学习时长")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name="封面", max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name="点击量")
    category = models.CharField(max_length=20, verbose_name="课程类别", default="后端开发")
    tag = models.CharField(max_length=15, verbose_name="课程标签", default="")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    you_need_know = models.CharField(max_length=300, default=u"一颗勤学的心是本课程必要前提",verbose_name=u"课程须知")
    teacher_tell = models.CharField(max_length=300, default=u"按时交作业,不然叫家长",verbose_name=u"老师告诉你")

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def get_chapter_nums(self):
        return self.lesson_set.all().count()
    get_chapter_nums.short_description = "章节数"

    def get_chapters(self):
        return self.lesson_set.all()

    def get_teacher_nums(self):
        return self.Teacher_set.all().count()



    def __str__(self):
        return "[{0}]的课程 >> {1}".format(self.course_org, self.name)

#章节
class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def get_lesson_videos(self):
        return self.video_set.all()

    def __str__(self):
        return "《{0}》课程的章节 >> {1}".format(self.course, self.name)

# 章节视频
class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name="章节")
    name = models.CharField(max_length=100, verbose_name="视频名称")
    url = models.CharField(max_length=200, default="http://blog.mtianyan.cn/", verbose_name=u"访问地址")
    learn_times = models.IntegerField(default=0, verbose_name="学习时长")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}章节的视频 >> {1}".format(self.lesson, self.name)


# 课程资源
class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="资源名称")
    download = models.FileField(upload_to="course/resouce/%Y/%m", verbose_name="资源文件", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}的资源文件 >> {1}".format(self.course, self.name)