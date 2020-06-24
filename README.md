[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# LiteratureRetrieval
基于智能语音芯片的文献自动检索系统

## 系统介绍
        本系统运行在Respeaker Core v2.0语音开发板上的文献自动检索系统，后端采用了Django框架，前端基于Vue以及Element-UI，爬虫的实现则采用了Scrapy框架。

## 环境配置及系统启动
    1. cd LiteratureRetrieval
    2. pip install -r requirements.txt // 安装依赖
    3. python manage.py makemigrations // 生成迁移文件， 需要先在settings.py文件中配置数据库
    4. python manage.py migrate // 同步到数据库
    5. celery worker -A taskproj -l info // 启动异步进程
    3. python manage.py runserver 127.0.0.0:8000 // 启动系统
    4. 在浏览器访问 http://127.0.0.1:8000
