from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [
    # url(r'^login_handle$',views.login_handle,name='login_handle'),

    url(r'^([0-9]+)/$',views.detail,name='detail'),
    url(r'^wirte_article/$',views.wirte_article,name='wirte_article'),
    url(r'^continue_wirte/([0-9]+)$',views.continue_wirte,name='continue_wirte'),
    url(r'^release_article/([a-zA-Z0-9]*)$',views.release_article,name='release_article'),
    url(r'^save_article/([a-zA-Z0-9]*)$',views.save_article,name='save_article'),
    url(r'^my_article/$',views.my_article,name='my_article'),
    url(r'^my_article/([0-9]+)$',views.my_article_detail,name='my_article_detail'),
    url(r'^del_article/([0-9]+)$',views.del_article,name='del_article'),
    url(r'^change_rel_status/([0-9]+)$',views.change_rel_status,name='change_rel_status'),
    url(r'^edit_article/([0-9]+)$',views.edit_article,name='edit_article'),
    url(r'^save_edit_article/([0-9]+)$',views.save_edit_article,name='save_edit_article'),
    # url(r'^textinput/$',views.textinput,name='textinput'),
    # url(r'^inputreturn/$',views.inputreturn,name='inputreturn'),
]