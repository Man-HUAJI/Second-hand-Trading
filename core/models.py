from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='分类名称')
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name='URL短名称')
    
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            self.slug = base_slug
            # 如果slug已存在，添加随机后缀
            counter = 1
            while Category.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{uuid.uuid4().hex[:4]}"
                counter += 1
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

# Item模型已迁移到items应用中
# 请使用items应用中的Item模型