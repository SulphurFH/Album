from django.db import models

# Create your models here.
class UserInfoManager(models.Manager):
    def create_userinfo(self,username,email):
        user = self.model()
        user.username = username
        user.email = email
        user.gender = True
        user.ispublicemail = True
        user.campany = ''
        user.address = ''
        user.about = ''
        user.url = ''
        # user.pic = ''
        user.avatar_address = ''
        return user

class UserInfo(models.Model):
    username = models.CharField(max_length=30,unique=True)
    email = models.CharField(max_length=254,blank=True)
    ispublicemail = models.BooleanField(default=0)
    gender = models.BooleanField()
    campany = models.CharField(max_length=30,blank=True)
    address = models.CharField(max_length=30,blank=True)
    about = models.TextField(blank=True)
    url = models.CharField(max_length=40,blank=True)
    pic = models.ImageField(upload_to='avatar/',height_field=200,width_field=200,blank=True)
    avatar_address = models.CharField(max_length=60,blank=True)

    users = UserInfoManager()

# 定义地区
class AreaInfo(models.Model):
    atitle = models.CharField(max_length=20)
    aParent = models.ForeignKey('self',null=True,blank=True)