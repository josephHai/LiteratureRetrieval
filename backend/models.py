from django.db import models


class Content(models.Model):
    title = models.CharField('标题', max_length=100, unique=True)
    authors = models.TextField('作者')
    brief = models.TextField('摘要')
    source = models.TextField('来源地址')
    website = models.TextField('来源网站')

    class Meta:
        verbose_name = u"文献内容"
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'Content<id=%s,name=%s>' % (
            self.id, self.title
        )


class Source(models.Model):
    short_name = models.CharField('网站简称', max_length=10)
    name = models.CharField('网站名称', max_length=50)
    url = models.CharField('网站地址', max_length=50)
    img_url = models.CharField('网站图标地址', max_length=50, default='http://s.c/static/img/source/default.jpg')

    class Meta:
        verbose_name = u"来源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'Source<id=%s,name=%s>' % (
            self.id, self.name
        )
