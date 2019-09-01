## flask-microblog
    python web框架 flask 学习项目

## venv虚拟环境安装
***Mac***
   * 参看 https://www.lizenghai.com/archives/8528.html

***Ubuntu***
   * 暂无  
   
***Windows***
   * 暂无

## venv 环境启动
***在项目根目录下***
* virtualenv --no-site-packages venv 生成当前项目的venv
* source venv/bin/activate  进入当前项目的venv
* deactivate                退出venv


## 线上环境部署（Ningx+Gunicorn）
* pip3 install virtualenv                  安装virtualenv
* cd /data/www/my_microblog
* which python3 -> /usr/bin/python3
* virtualenv -p /usr/bin/python3 venv      在项目根目录下生成 virtualenv相关的环境文件，已有就不再生成



## 启动线上服务
* cd /data/www/my_microblog
* . venv/bin/activate                          开启virtualenv
* gunicorn -w 4 -b 127.0.0.1:5000 run:app      开启gunicorn
* service nginx start                          开启nginx

## 调试注意点记录
***邮件***
* 终端1 python3 -m smtpd -n -c DebuggingServer localhost:8025
* 终端2 set MAIL_SERVER=localhost     set MAIL_PORT=8025

***requirements.txt 自动生成***
* pip3 freeze > requirements.txt

## 语言本地化
***flask—babel 安装使用翻译功能***
* pip安装flask-babel扩展
* 根目录下添加配置文件babel.cfg
   - [python: app/**.py]
   - [jinja2: app/templates/**.html]
   - extensions=jinja2.ext.autoescape,jinja2.ext.with_
* cd /data/www/my_microblog
* pybabel extract -F babel.cfg -k _l -o messages.pot .   根据babel.cfg 读取_()_l()标记的代码和模版，生成.pot文件
* pybabel init -i messages.pot -d app/translations -l zh  生成中文语言目录及相关的对照翻译文档.po
* pybabel compile -d app/translations                   编译.po文件生成.mo文件，用于应用加载翻译

***flask—babel 更新翻译***
* cd /data/www/my_microblog
* pybabel extract -F babel.cfg -k _l -o messages.pot .   
* pybabel update -i messages.pot -d app/translations
* pybabel compile -d app/translations  

***flask—babel 翻译函数使用***
* _() 用于request,如route .html中
* _l() 用于form中 from flask_babel import lazy_gettext as _l
* _('Hi,%(username)s.Welcome to login!',username=current_user.username)) 其中%(username)s是格式符号

## 添加自定义flask命令
* import click 添加命令行参数 
   - @click.argument('lang')
* import app.cli 添加自定义命令
   - @app.cli.group(name='自定义命令组名称',help='命令组功能描述') 添加命令组
   - @自定义命令组名称.command(name='自定义命令',help='命令功能描述')
* 必须将自定义命令command.py 导入到入口脚本中(run.py)
* 自定义命令组使用
   - flask 自定义命令组名称 自定义命令 参数
 
   
                                                                                       