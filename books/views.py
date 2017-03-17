import time
import os
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from markdown import markdown
from books.models import BookInfo,UserInfo


#@login_required
def detail(request,id):
    username = request.session.get('username')

    if request.user.is_authenticated():
        signIn = True
    else:
        signIn = False

    bookslist = BookInfo.books.filter(isrelease=1).order_by('-bpub_date')[0:50]

    book = BookInfo.books.filter(id=id)[0]
    bookname = book.btitle
    authorname = UserInfo.users.filter(id=book.user.id)[0].username

    bookhtml = book.bhtml

    if username:
        avatarPath = settings.MEDIA_ROOT + '/avatar/' + username + '.jpg'
        if os.path.exists(avatarPath):
            avatarExist = True
        else:
            avatarExist = False
    else:
        avatarExist = False

    # 校验用户登录方式，分别展示PC或移动端页面
    agent = request.META['HTTP_USER_AGENT'].lower().find('mobile')
    if agent > 0:
        return render(request, 'books/detail_modile.html',
                      {'bookname': bookname, 'bookslist': bookslist,'bookhtml':bookhtml,
                       'signIn':signIn,'username':username,'authorname':authorname,'avatarExist':avatarExist})
    else:
        return render(request, 'books/detail.html',
                  {'bookname': bookname, 'bookslist': bookslist,'bookhtml':bookhtml,
                   'signIn':signIn,'username':username,'authorname':authorname,'avatarExist':avatarExist})

@login_required
@csrf_exempt
def wirte_article(request):
    username = request.session.get('username')
    # 判断用户登录状态，agent>0不是电脑登录
    agent = request.META['HTTP_USER_AGENT'].lower().find('mobile')
    if agent > 0:
        return render(request,'books/wirtearticle_mobile.html',{'username':username})
    else:
        return render(request, 'books/wirtearticle.html', {'username': username})


@login_required
@csrf_exempt
def release_article(request,savebook=False):
    username = request.session.get('username')
    email = request.session.get('email')
    text = request.POST['content']
    title = request.POST['arttitle']
    agent = request.META['HTTP_USER_AGENT'].lower().find('mobile')
    # 校验文章标题不能为空
    if title is '':
        noTitle = True
        if agent > 0:
            return render(request, 'books/wirtearticle_mobile.html',
                          {'username': username, 'noTitle': noTitle, 'text': text})
        else:
            return render(request, 'books/wirtearticle.html',
                          {'username': username, 'noTitle': noTitle, 'text': text})
    elif len(title) > 40:
        longTitle = True
        if agent > 0:
            return render(request, 'books/wirtearticle_mobile.html',
                          {'username': username, 'longTitle': longTitle, 'text': text,'title':title})
        else:
            return render(request, 'books/wirtearticle.html',
                          {'username': username, 'longTitle': longTitle, 'text': text,'title':title})
    else:
        # 文章内容渲染成html格式
        html = markdown(text, extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite'])

        if savebook:
            book = BookInfo.books.filter(id=savebook)[0]
            book.btitle = title
            book.bcontent = text
            book.bhtml = html
            book.isrelease = True
            book.save()
            return redirect(reverse('users:userinfo', args=(username,)))
        else:
            userid = UserInfo.users.filter(email=email)[0].id

            # 将文章存入数据库
            createBook = BookInfo.books.create_book(username, title,
                                                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                    text, html, userid, True)
            createBook.save()
            return redirect(reverse('users:userinfo', args=(username,)))


@login_required
@csrf_exempt
def save_article(request,savebook=False):
    username = request.session.get('username')
    email = request.session.get('email')
    text = request.POST['content']
    title = request.POST['arttitle']
    agent = request.META['HTTP_USER_AGENT'].lower().find('mobile')
    if title is '':
        noTitle = True
        if agent > 0:
            return render(request,'books/wirtearticle_mobile.html',
                          {'username':username,'noTitle':noTitle,'text':text})
        else:
            return render(request, 'books/wirtearticle.html',
                          {'username': username, 'noTitle': noTitle, 'text': text})
    elif len(title) > 40:
        longTitle = True
        if agent > 0:
            return render(request, 'books/wirtearticle_mobile.html',
                          {'username': username, 'longTitle': longTitle, 'text': text,'title':title})
        else:
            return render(request, 'books/wirtearticle.html',
                          {'username': username, 'longTitle': longTitle, 'text': text,'title':title})
    else:
        #文章内容渲染成html格式
        html = markdown(text,extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite'])

        if savebook:
            book = BookInfo.books.filter(id=savebook)[0]
            book.btitle = title
            book.bcontent = text
            book.bhtml = html
            book.save()
            return redirect(reverse('books:continue_wirte', args=(savebook,)))
        else:
            userid = UserInfo.users.filter(email=email)[0].id

            #将文章存入数据库
            createBook = BookInfo.books.create_book(username,title,time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                    text,html,userid,False)
            createBook.save()
            bookid = createBook.pk
            return redirect(reverse('books:continue_wirte',args=(bookid,)))


@login_required
@csrf_exempt
def continue_wirte(request,bookid):
    bookinfo = BookInfo.books.filter(pk=bookid)[0]
    username = bookinfo.bauthor
    title = bookinfo.btitle
    content = bookinfo.bcontent

    agent = request.META['HTTP_USER_AGENT'].lower().find('mobile')
    if agent > 0:
        return render(request, 'books/wirtearticle_mobile.html', {'bookid':bookid,'username': username,
                                                                  'title':title,'content':content})
    else:
        return render(request, 'books/wirtearticle.html', {'bookid':bookid,'username': username,
                                                           'title':title,'content':content})

# 个人文章首页
@login_required
def my_article(request):
    if request.user.is_authenticated():
        username = request.session.get('username')
        avatarPath = settings.MEDIA_ROOT + '/avatar/' + username + '.jpg'
        if os.path.exists(avatarPath):
            avatarExist = True
        else:
            avatarExist = False
        bookslist = BookInfo.books.filter(bauthor=username).order_by('-bpub_date')
        return render(request,'books/my_article.html',{'username':username,'bookslist':bookslist,'avatarExist':avatarExist})

# 个人文章详细页
@login_required
def my_article_detail(request,bookid):
    if request.user.is_authenticated():
        username = request.session.get('username')

        bookslist = BookInfo.books.filter(bauthor=username).order_by('-bpub_date')
        book = BookInfo.books.filter(id=bookid)[0]

        avatarPath = settings.MEDIA_ROOT + '/avatar/' + username + '.jpg'
        if os.path.exists(avatarPath):
            avatarExist = True
        else:
            avatarExist = False

        return render(request,'books/my_article_detail.html',{'username':username,'bookslist':bookslist,
                                                              'book':book,'avatarExist':avatarExist,'bookid':bookid})
    else:
        return redirect(reverse('users:signin'))

# 逻辑删除文章
@login_required
def del_article(request,bookid):
    if request.user.is_authenticated():
        book = BookInfo.books.get(pk=bookid)
        book.isDelete = True
        book.save()
        return redirect(reverse('books:my_article'))
    else:
        return redirect(reverse('users:signin'))

#
@login_required
def change_rel_status(request,bookid):
    if request.user.is_authenticated():
        book = BookInfo.books.get(pk=bookid)
        if book.isrelease:
            book.isrelease = False
        else:
            book.isrelease = True
        book.save()
        return redirect(reverse('books:my_article_detail',args=(bookid,)))
    else:
        return redirect(reverse('users:signin'))

@login_required
def edit_article(request,bookid):
    if request.user.is_authenticated():
        book = BookInfo.books.get(pk=bookid)
        username = request.session.get('username')
        return render(request,'books/edit_my_article.html',{'book':book,'username':username,'bookid':bookid})
    else:
        return redirect(reverse('users:signin'))

@login_required
def save_edit_article(request,bookid):
    if request.user.is_authenticated():
        username = request.session.get('username')
        book = BookInfo.books.get(pk=bookid)
        title = request.POST['arttitle']
        content = request.POST['content']
        if title is '':
            noTitle = True
            return render(request, 'books/edit_my_article.html',
                          {'username': username, 'noTitle': noTitle, 'content': content,'bookid':bookid})
        elif len(title) > 40:
            longTitle = True
            return render(request, 'books/edit_my_article.html',
                          {'username': username, 'longTitle': longTitle,
                           'content': content, 'title': title,'bookid':bookid})
        else:
            # 文章内容渲染成html格式
            html = markdown(content, extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite'])

            book.btitle = title
            book.bcontent = content
            book.bhtml = html
            book.isrelease = True
            book.save()

            return redirect(reverse('books:my_article'))