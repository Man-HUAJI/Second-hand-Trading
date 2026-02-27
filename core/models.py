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

class Item(models.Model):
    title = models.CharField(max_length=200, verbose_name='物品标题')
    description = models.TextField(verbose_name='物品描述')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='价格')
    image = models.ImageField(upload_to='items/', null=True, blank=True, verbose_name='物品图片')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='发布者')
    
    class Meta:
        verbose_name = '物品'
        verbose_name_plural = '物品'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title