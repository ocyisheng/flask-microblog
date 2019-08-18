# flask-microblog

# venv虚拟环境安装
    ## Mac
        *https://www.lizenghai.com/archives/8528.html

    ## Ubuntu

    ## Windows


# venv 环境启动
    ## 在项目根目录下
        *virtualenv --no-site-packages venv 当前项目的venv
        *source venv/bin/activate  进入当前项目的venv
        *deactivate                退出venv


# 线上环境部署（Ningx+Gunicorn）
    ** pip3 install virtualenv                  安装virtualenv
    ** cd /root/www/my_microblog
    ** which python3 -> /usr/bin/python3
    ** virtualenv -p /usr/bin/python3 venv      在项目根目录下生成 virtualenv相关的环境文件，已有就不再生成



# 启动线上服务
    ** cd /root/www/my_microblog
    ** . venv/bin/activate                          开启virtualenv
    ** gunicorn -w 4 -b 127.0.0.1:5000 run:app      开启gunicorn
    ** service nginx start
