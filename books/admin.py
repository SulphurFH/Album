from django.contrib import admin
from .models import BookInfo,HeroInfo,BooksAdmin,HerosAdmin

# Register your models here.
# 注册模型并添加到admin中
admin.site.register(BookInfo,BooksAdmin)
admin.site.register(HeroInfo,HerosAdmin)