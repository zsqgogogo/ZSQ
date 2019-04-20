import os

from django.template import loader

from celery_tasks.main import app
from mall import settings
from utils.goods import get_categories
@app.task(name='generate_static_list_search_html')
def generate_static_list_search_html():
    categories=get_categories()
    context={
        'categories':categories
    }
    #设置模板
    tempalte=loader.get_template('list.html')
    #给模板填充数据

    html_text=tempalte.render(context)
    #保存到路径里面去
    file_path=os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR,'list.html')
    with open(file_path,'w') as f:
        f.write(html_text)