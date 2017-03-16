from django.db import models
from users.models import UserInfo
from django.contrib import admin

# Create your models here.

class BookInfoManager(models.Manager):
    # 重写get_queryset方法，返回Book中isDelete字段是FALSE的值
    def get_queryset(self):
        # 另一种表示的super方法，个人感觉不如下面一种好记
        #return super(BookInfoManager, self).get_queryset().filter(isDelete=False)
        return super().get_queryset().filter(isDelete=False)

    # 创建文章的方法，可以通过BookInof.books.create_book()调用
    def create_book(self,bauthor,btitle,bpub_date,bcontent,bhtml,user_id,isrelease):
        book = self.model()
        book.btitle = btitle
        book.bpub_date = bpub_date
        book.bauthor = bauthor
        book.bread = 0
        book.isDelete = False
        book.bcontent = bcontent
        book.bhtml = bhtml
        book.user_id = user_id
        book.isrelease = isrelease
        return book

# 定义文章
class BookInfo(models.Model):
    btitle = models.CharField(max_length=40)
    bauthor = models.CharField(max_length=15)
    bpub_date = models.DateTimeField()
    # 默认0，0：没有读，1：读过
    bread = models.IntegerField(default=0)
    bcontent = models.TextField(blank=True)
    bhtml = models.TextField(blank=True)
    # 是否发布，0：没有发布，1：已发布
    isrelease = models.BooleanField()
    # 逻辑删除，默认0，0：没有删除，1：删除
    isDelete = models.BooleanField(default=False)
    # 关联User表
    user = models.ForeignKey(UserInfo)

    # 这里重写设定objects对象，objects对象负责与数据库交互，默认是objects，比如BookInfo.objects.all(),
    # 在这里修改后为BookInfo.books.all()的方式交互
    books = BookInfoManager()
    def __str__(self):
        return "%d"%self.pk

class BooksAdmin(admin.ModelAdmin):
    list_display = ['pk', 'btitle', 'bauthor','bpub_date']
    list_filter = ['bauthor','btitle']
    list_per_page = 10

# 定义英雄
class HeroInfo(models.Model):
    hname = models.CharField(max_length=20)
    hgender = models.BooleanField()
    hcontent = models.CharField(max_length=200)
    # 逻辑删除，默认0，0：没有删除，1：删除
    isDelete = models.BooleanField(default=False)
    hbook = models.ForeignKey(BookInfo)

    def __str__(self):
        return "%d"%self.pk

class HerosAdmin(admin.ModelAdmin):
    list_display = ['pk','hname','hcontent']