from celery import Celery
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mall.settings'
#创建Celery对象
#参数main 设置脚本名
app = Celery('celery_tasks')

#加载配置文件
app.config_from_object('celery_tasks.config')
app.autodiscover_tasks(['celery_tasks.sms','celery_tasks.html'])



"""
1.要想使用celery，必须使用工程的配置文件，（参照manage.py）
2.创建celery实例对象，参数main可以理解为名字，唯一就好了。一般可以设置为包名
3.设置broker，app.config_from_object('celery_tasks.config')参数是配置文件路径
4.celery自动检测  app.autodiscover_tasks(['tasks任务路径'])
"""