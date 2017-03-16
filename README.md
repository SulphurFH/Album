# Album

##环境搭建

###virtualenv创建

根据自己环境中Python3位置创建
virtualenv -p /usr/bin/python3 album_papers

###pip安装组件

pip install -r requirements.txt

###修改数据库连接

album_papers/settings.py

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'databasename',
        'USER': 'username',
        'PASSWORD': 'password',
        'HOST': 'ip',
        'PORT': '3306',
    }
}
```

###whoosh配置

拷贝requirement/whoosh下的ChineseAnalyzer.py和whoosh_cn_backend.py文件到haystack安装路径的backends下
默认是在虚拟环境安装包的地址，如：virtualenv/django1.8_py3/lib/python3.6/site-packages/haystack/backends

###同步数据库及索引

进入虚拟环境
如：source virtualenv/django1.8_py3/bin/activate
切换至项目路径
cd Album
执行数据库同步命令
python manage.py syncdb
执行生成索引命令
python manage.py rebuild_index
