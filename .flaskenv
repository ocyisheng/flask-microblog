# 解决flask 1.x 线上环境切换

# 程序运行入口文件
FLASK_APP=run.py

# 运行环境
# 测试 development
FLASK_ENV=development

# 运行状态 True
# 生产环境必须为False
FLASK_DEBUG=True


# 数据库路径
# DATABASE_URI=


## 邮件本地测试
## python3 -m smtpd -n -c DebuggingServer localhost:8025

#MAIL_PORT=8025
#MAIL_SERVER=localhost
#FLASK_DEBUG=False