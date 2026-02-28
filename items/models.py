from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid


class Category(models.Model):
    """物品分类模型"""
    name = models.CharField(max_length=100, verbose_name='分类名称')
    slug = models.SlugField(max_length=100, unique=True, blank=True, verbose_name='URL标识')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # 生成唯一的slug
            base_slug = slugify(self.name)
            self.slug = base_slug
            counter = 1
            while Category.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Item(models.Model):
    """物品模型"""
    
    # 交易方式选项
    TRADE_METHOD_CHOICES = [
        ('face_to_face', '面交'),
        ('shipping', '邮寄'),
        ('both', '均可'),
    ]
    
    # 物品状态选项
    CONDITION_CHOICES = [
        ('new', '全新'),
        ('used', '二手'),
        ('idle', '闲置'),
    ]
    
    # 物品状态选项
    STATUS_CHOICES = [
        ('active', '在售'),
        ('sold', '已售'),
        ('inactive', '下架'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='物品标题')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='物品分类')
    description = models.TextField(verbose_name='详细描述')
    trade_method = models.CharField(
        max_length=20, 
        choices=TRADE_METHOD_CHOICES, 
        default='face_to_face',
        verbose_name='交易方式'
    )
    contact = models.CharField(max_length=100, verbose_name='联系方式')
    condition = models.CharField(
        max_length=20, 
        choices=CONDITION_CHOICES, 
        default='used',
        verbose_name='物品状态'
    )
    image = models.ImageField(
        upload_to='items/', 
        blank=True, 
        null=True, 
        verbose_name='物品图片'
    )
    seller = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='发布者')
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='active',
        verbose_name='物品状态'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '物品'
        verbose_name_plural = '物品'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['category']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.seller.username}"
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('item_detail', kwargs={'pk': self.pk})
    
    def get_image_url(self):
        """获取物品图片URL，如果没有图片则返回默认图片"""
        if self.image:
            return self.image.url
        else:
            return '/static/images/DefaultProfile_256.png'