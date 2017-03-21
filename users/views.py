import os

from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse
# from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from users.models import UserInfo
from books.models import BookInfo
# from hashlib import sha1
# from redis_db.RedisHelper import RedisHelper
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib.auth.hashers import check_password
from django.conf import settings

# Create your views here.
# 登录
def signin(request):
    return render(request, 'users/sign.html')

# 注册
def register(request):
    return render(request, 'users/register.html')

# 设置session
def login_handle(request):
    request.session['email'] = request.POST['email']
    request.session['passwd'] = request.POST['passwd']

    # 设置session超时设定10s后过期
    # request.session.set_expiry(10)
    # 设置session超时设定关闭浏览器后过期
    request.session.set_expiry(0)
    return redirect(reverse('users:index'))

# def islogin(request):
#     if request.user.is_authenticated():
#         username = request.session.get('username')
#         avatarPath = settings.MEDIA_ROOT + '/avatar/' + username + '.jpg'
#         if os.path.exists(avatarPath):
#             address = '/static/media/avatar/'+ username +'.jpg'
#             data = {'status': 1,'info': {'name': username,'avatar': address}}
#         else:
#             # data = {'status': 1,'info': {'name': username,'avatar': '/static/media/avatar/novavtar.jpg'}}
#             data = {'status': 1, 'info': {'name': username, 'avatar': None}}
#         return JsonResponse(data)
#     else:
#         # data = {'status':0,'info': {'name': None,'avatar':'/static/media/avatar/novavtar.jpg'}}
#         data = {'status': 0, 'info': {'name': None, 'avatar': None}}
#         return JsonResponse(data)

# 退出清除session
def logout(request):
    request.session.flush()
    return redirect(reverse('users:signin'))


# 文章主页
def index(request):
    # 获取所有文章
    bookslist = BookInfo.books.filter(isrelease=1).order_by('-bpub_date')[0:50]
    # 获取session中的邮箱地址和密码
    email = request.session.get('email')
    passwd = request.session.get('passwd')
    agent = request.META['HTTP_USER_AGENT'].lower().find('mobile')

    if email is None or passwd is None:
        signIn = None
        # 校验用户登录方式，分别展示PC或移动端页面
        if agent > 0:
            return render(request, 'books/first_page_modile.html', {'bookslist': bookslist, 'signIn': signIn})
            # return render(request, 'books/first_page_modile.html', {'bookslist': bookslist})
        else:
            return render(request, 'books/first_page.html', {'bookslist': bookslist, 'signIn': signIn})
            # return render(request, 'books/first_page.html', {'bookslist': bookslist})
    else:
        if not User.objects.filter(email=email):
            notExistEmail = True
            return render(request, 'users/sign.html', {'notExistEmail': notExistEmail})
        else:
            # django用户认证
            username = User.objects.filter(email=email)[0].username
            user = authenticate(username=username, password=passwd)
            request.session['username'] = username
            # 登录
            if user:
                if user.is_active:
                    login(request, user)
                    signIn = True

                    # 校验用户登录方式，分别展示PC或移动端页面
                    if agent > 0:
                        return render(request, 'books/first_page_modile.html', {'bookslist': bookslist, 'signIn': signIn,
                                                                                'username': username})
                    else:
                        avatarPath = settings.MEDIA_ROOT + '/avatar/' + username + '.jpg'
                        if os.path.exists(avatarPath):
                            avatarExist = True
                        else:
                            avatarExist = False
                        return render(request, 'books/first_page.html', {'bookslist': bookslist, 'signIn': signIn,
                                                                         'username': username,'avatarExist':avatarExist})
                else:
                    notActive = True
                    return render(request, 'users/sign.html', {'notActive': notActive})
            else:
                worngPasswd = True
                return render(request, 'users/sign.html', {'worngPasswd': worngPasswd})

# 注册状态验证
def status(request):
    username = request.POST['username']
    email = request.POST['email']
    passwd = request.POST['passwd']
    confirmpasswd = request.POST['confirmpasswd']

    if username is '':
        userNotNull = True
        return render(request,'users/register.html',{'userNotNull':userNotNull})
    elif  passwd is '':
        passwdNotNull = True
        return render(request, 'users/register.html', {'passwdNotNull': passwdNotNull})
    elif  email is '':
        emailNotNull = True
        return render(request, 'users/register.html', {'emailNotNull': emailNotNull})
    else:

        if User.objects.filter(username=username):
                isuserexist = True
                return render(request,'users/register.html',{'isuserexist':isuserexist,'username':username})
        elif User.objects.filter(email=email):
                isemailexist = True
                return render(request, 'users/register.html', {'isemailexist': isemailexist, 'email': email})
        elif passwd == confirmpasswd:

            # 用户认证信息存入User
            user = User.objects.create_user(username, email, passwd)
            user.save()

            # 用户信息存入UserInfo
            userinfo = UserInfo.users.create_userinfo(username,email)
            userinfo.save()

            # redis缓存 django中用户登录认证的session和cookie还需要再确认再添加至redis
            # shapwd = User.objects.filter(username=username)[0].password
            # redis_userdata = RedisHelper('192.168.100.128', 6379)
            # redis_userdata.set(email, shapwd)

            registersucess = True
            return render(request, 'users/sign.html',{'registersucess':registersucess})
        else:
            isconfirmpasswd = True
            return render(request, 'users/register.html', {'isconfirmpasswd': isconfirmpasswd})

# 用户信息
@login_required
def userinfo(request,username):
    userid = UserInfo.users.filter(username=username)[0].id
    agent = request.META['HTTP_USER_AGENT'].lower().find('mobile')

    bookinfo = BookInfo.books.all().filter(user_id=userid).order_by('-bpub_date')[0:6]
    contentList = []
    for content in bookinfo:
        contentList.append(content.bcontent[0:30])

    avatarPath = settings.MEDIA_ROOT + '/avatar/' + username + '.jpg'
    if os.path.exists(avatarPath):
        avatarExist = True
    else:
        avatarExist = False

    if agent > 0:
        email = request.session.get('email')
        return render(request,'users/userinfo_mobile.html',{'username':username,'bookinfo':bookinfo,
                                                            'contentList':contentList,'email':email,'avatarExist':avatarExist})
    else:
        return render(request, 'users/userinfo.html', {'username': username, 'bookinfo': bookinfo,
                                                       'contentList': contentList,'avatarExist':avatarExist})

@login_required
def edit_userinfo(request,username):
    userinfo = UserInfo.users.filter(username=username)[0]

    avatarPath = settings.MEDIA_ROOT + '/avatar/' + username + '.jpg'
    if os.path.exists(avatarPath):
        avatarExist = True
    else:
        avatarExist = False

    return render(request,'users/edit_userinfo.html',{'username':username,'userinfo':userinfo,'avatarExist':avatarExist})

@login_required
def update_userinfo(request,userid):
    new_username = request.POST['newusername']
    old_username = User.objects.filter(email=request.session.get('email'))[0].username
    userAuth = User.objects.filter(username=new_username)

    # 判断性别的True和False
    gender = request.POST['gender']
    if gender == '0':
        gender = False
    else:
        gender = True

    # 判断公开邮箱的True和False
    ispublicemail = request.POST['ispublicemail']
    if ispublicemail == '0':
        ispublicemail = False
    else:
        ispublicemail = True

    about = request.POST['about']
    url = request.POST['url']
    campany = request.POST['campany']
    address = request.POST['address']

    if len(userAuth) == 0:
        userAuth = User.objects.filter(username=old_username)[0]
        userAuth.username = new_username
        userAuth.save()

        userinfo = UserInfo.users.filter(id=userid)[0]

        # 用户头像改名
        oldAvatarPath = settings.MEDIA_ROOT + '/avatar/' + old_username + '.jpg'
        newAvatarPath = settings.MEDIA_ROOT + '/avatar/' + new_username + '.jpg'
        os.rename(oldAvatarPath, newAvatarPath)

        # 用户信息添加至userinfo表
        avatar_address = '/static/media/avatar/' + new_username + '.jpg'
        userinfo.username,userinfo.gender,userinfo.ispublicemail,userinfo.about,userinfo.url,userinfo.campany,\
        userinfo.address,userinfo.avatar_address = new_username,gender,ispublicemail,about,url,campany,address,avatar_address
        userinfo.save()

        data = {'status': 1,'username':new_username}
        return JsonResponse(data)
    elif len(userAuth) == 1 and new_username == old_username:
        userinfo = UserInfo.users.filter(id=userid)[0]

        # 用户信息添加至userinfo表
        userinfo.gender, userinfo.ispublicemail, userinfo.about, userinfo.url, userinfo.campany, \
        userinfo.address = gender, ispublicemail, about, url, campany, address
        userinfo.save()

        data = {'status': 1, 'username': new_username}
        return JsonResponse(data)
    else:
        data = {'status':3}
        return JsonResponse(data)

@login_required
def change_password(request,username):
    user = User.objects.get(username=username)
    user_password = user.password
    # 获取POST表单内密码
    old_password = request.POST['oldpassword']
    new_password = request.POST['newpassword']
    confirm_password = request.POST['confpassword']

    if new_password == confirm_password:
        # 验证原密码是否正确
        passwdCorrect = check_password(old_password,user_password)
        if passwdCorrect:
            user.set_password(new_password)
            user.save()
            # 更新完密码后登出刷新sessions
            data = {'status':1}
            return JsonResponse(data)
        else:
            data = {'status':2}
            return JsonResponse(data)
    else:
        data = {'status': 3}
        return JsonResponse(data)
@login_required
def upload_avatar(request,username):
    if request.method == "POST":
        try:
            f1 = request.FILES['pic']
            f1.name = username + '.jpg'
            fname = '%s/avatar/%s' % (settings.MEDIA_ROOT, f1.name)

            with open(fname, 'wb') as pic:
                for c in f1.chunks():
                    pic.write(c)

            userinfo = UserInfo.users.get(username=username)
            userinfo.avatar_address = '/static/media/avatar/' + f1.name
            userinfo.save()

            return redirect(reverse('users:edit_userinfo', args=(username,)))
        except Exception as error:
            print(error)
            return redirect(reverse('users:edit_userinfo', args=(username,)))
    else:
        return redirect(reverse('users:edit_userinfo', args=(username,)))

def about_user(request,checkuser):
    try:
        username = UserInfo.users.filter(email=request.session.get('email'))[0].username
    except IndexError as error:
        print(error)
    checkuserinfo = UserInfo.users.get(username=checkuser)
    if checkuser == username:
        bookinfo = BookInfo.books.all().filter(bauthor=checkuser).order_by('-bpub_date')
    else:
        bookinfo = BookInfo.books.all().filter(bauthor=checkuser,isrelease=1).order_by('-bpub_date')

    return render(request, 'users/about_user.html', {'checkuser': checkuser, 'username': username,
                                                     'checkuserinfo':checkuserinfo,'bookinfo': bookinfo})
