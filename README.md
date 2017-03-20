# Album

## 1.开发环境搭建

### virtualenv创建

根据自己环境中Python3位置创建

```bash
virtualenv -p /usr/bin/python3 django1.8_py3
```

### pip安装组件

```bash
source django1.8_py3/bin/activate
pip install -r requirements.txt
```

### 修改数据库连接

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

### whoosh配置

拷贝requirement/whoosh下的ChineseAnalyzer.py和whoosh_cn_backend.py文件到haystack安装路径的backends下
默认是在虚拟环境安装包的地址，如：virtualenv/django1.8_py3/lib/python3.6/site-packages/haystack/backends

### 同步数据库及索引

进入虚拟环境

```bash
如：source virtualenv/django1.8_py3/bin/activate
```

切换至项目路径

```bash
cd Album
```

执行数据库同步命令

```bash
python manage.py syncdb
python manage.py makemigrations
python manage.py migrate
```
如果报权限不足的错误可以尝试看一下上传项目文件夹的权限

```bash
chown -R user:group Album
```

执行生成索引命令

```bash
python manage.py rebuild_index
```
### 启动命令

```bash
python manage.py runserver ip:port
```

## 2.生产环境搭建
### python3安装
```bash
sudo apt-get install python3
sudo apt-get install python3-dev
```
如果已安装以上两个可以跳过

### pip安装
```bash
sudo apt-get install python-pip
```
### virtualenv安装
```bash
sudo apt-get install python-virtualenv
```
### virtualenv创建

根据自己环境中Python3位置创建

```bash
virtualenv -p /usr/bin/python3 django1.8_py3
```

### pip安装组件

```bash
source django1.8_py3/bin/activate
pip install -r requirements.txt
```

### 修改数据库连接

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

### whoosh配置

拷贝requirement/whoosh下的ChineseAnalyzer.py和whoosh_cn_backend.py文件到haystack安装路径的backends下
默认是在虚拟环境安装包的地址，如：virtualenv/django1.8_py3/lib/python3.6/site-packages/haystack/backends

### 同步数据库及索引

进入虚拟环境

```bash
如：source virtualenv/django1.8_py3/bin/activate
```

切换至项目路径

```bash
cd Album
```

执行数据库同步命令

```bash
python manage.py syncdb
python manage.py makemigrations
python manage.py migrate
```
如果报权限不足的错误可以尝试看一下上传项目文件夹的权限

```bash
chown -R user:group Album
```

执行生成索引命令

```bash
python manage.py rebuild_index
```

### 启动命令

```bash
python manage.py runserver ip:port
```
测试连接无误之后进行uWSGI+Nginx配置

### 安装uWSGI
进入项目虚拟环境

```bash
source virtualenv/django1.8_py3/bin/activate
pip install uwsgi
```
在项目根目录下创建uwsgi.ini文件，内容如下

```bash
[uwsgi]
socket=127.0.0.1:3031 #使用nginx连接用socket
#http=192.168.0.105:8000
chdir=/home/fangho/Desktop/www/Album #项目所在路径
wsgi-file=album_papers/wsgi.py #项目中wsgi.py文件所在路径
processes=4
threads=2
master=True
pidfile=uwsgi.pid
daemonize=uwsgi.log
```

### 安装Nginx
```bash
sudo apt-get install nginx
```
修改nginx配置文件

```bash
cd /etc/nginx/sites-available
cp default default_bak
vim default
```

内容如下：

```bash
server {
	listen 80; #外网访问项目端口
	server_name 192.168.0.105; #外网IP

	location / {
	include uwsgi_params; #将所有的参数转到uwsgi下
	uwsgi_pass 127.0.0.1:3031; #uwsgi的ip与端口;
	}

	location /static {
    	alias /var/www/Album/static/; #Nginx代理静态文件地址，需要自己手动创建
	}
}

```

### 项目文件修改

```bash
cd Album/album_papers
vim settings.py
1.修改DEBUG=True
	修改为DEBUG=False
2.指定HOST地址，及服务器外网地址
	ALLOWED_HOSTS = []
3.制定静态文件地址，此地址与Nginx中的一致
	STATIC_ROOT='/var/www/Album/static/'
```

### 创建项目静态文件目录

```bash
cd /var/www/
mkdir -p Album/static/
chmod 777 Album
```

### 收集所有静态文件到static_root指定目录
```bash
source virtualenv/django1.8_py3/bin/activate
cd Album/album_papers
python manage.py collectstatic
```

### 启动Nginx、uWSGI
1.Nginx

```bash
sudo /etc/init.d/nginx start #启动
sudo /etc/init.d/nginx stop #停止
sudo /etc/init.d/nginx restart #重启
```

2.uWSGI

```bash
source virtualenv/django1.8_py3/bin/activate
cd Album/

uwsgi --ini uwsgi.ini #启动
uwsgi --stop uwsgi.pid #停止
uwsgi --reload uwsgi.pid #重启
```