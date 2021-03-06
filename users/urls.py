from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$',views.signin,name='signin'),
    url(r'^register$',views.register,name='register'),
    url(r'^registerName/$',views.registerName,name='registerName'),
    url(r'^registerEmail/$',views.registerEmail,name='registerEmail'),
    url(r'^status/$',views.status,name='status'),
    url(r'^login_handle$',views.login_handle,name='login_handle'),
    url(r'^index/$', views.index, name='index'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^userinfo/([\w\W]+)$',views.userinfo,name='userinfo'),
    url(r'^aboutuser/([\w\W]+)$',views.about_user,name='about_user'),
    url(r'^edit_userinfo/([a-zA-Z0-9\.@]+)$',views.edit_userinfo,name='edit_userinfo'),
    url(r'^update_userinfo/([0-9\.@]+)$',views.update_userinfo,name='update_userinfo'),
    url(r'^change_password/([a-zA-Z0-9\.@]+)$',views.change_password,name='change_password'),
    url(r'^upload_avatar/([a-zA-Z0-9\.@]+)$',views.upload_avatar,name='upload_avatar'),
]