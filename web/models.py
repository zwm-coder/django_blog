import re

import markdown
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.html import strip_tags


class MyAuthor(AbstractUser):
    avatar = models.CharField(max_length=255)
    nick_name = models.CharField(max_length=200)
    desc = models.CharField(max_length=255)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    excerpt = models.CharField(max_length=200, blank=True)
    cover_img = models.CharField(max_length=200, blank=True)
    author = models.ForeignKey(MyAuthor, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    add_date = models.DateField()
    mod_date = models.DateField()

    class Meta:
        ordering = ('-add_date',)

    def __str__(self):
        return self.title

    # 复写save方法实现自动生成文章摘要和自动提取封面图片
    def save(self, *args, **kwargs):
        if not self.excerpt or not self.cover_img:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])

            # 先将Markdowb文本渲染成HTML文本
            html_doc = md.convert(self.content)
            image = re.search(re.compile('<img.+src="(.+)" />'), html_doc)
            if image:
                self.cover_img = image.group(1)
                print(self.cover_img)
                print(image.group(1))
            # 利用strip_tags去掉HTML文本的全部HTML标签
            self.excerpt = strip_tags(md.convert(self.content))[:80]

        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def get_next_article(self):
        next_article = Article.objects.filter(pk=self.pk+1).first()
        if not next_article:
            return False
        return next_article

    def get_previous_article(self):
        previous_article = Article.objects.filter(pk=self.pk - 1).first()
        if not previous_article:
            return False
        return previous_article
