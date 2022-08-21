from celery import Celery
# 初始化celery对象
app = Celery("renran")

# 初始化django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'renranapi.settings.dev')
import django
django.setup()

# 加载配置
app.config_from_object("mycelery.config")

# 注册异步任务
# 任务以包进行管理,每一个包必须里面包含了一个tasks.py文件
app.autodiscover_tasks(["mycelery.sms","mycelery.article"])

# 在终端下面运行celery,将来在线上服务器中,可以使用supervisor以守护进程的方式启动
# celery -A mycelery.main worker --loglevel=info