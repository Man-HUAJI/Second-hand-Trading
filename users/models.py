from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Profile(models.Model):
    """用户扩展信息模型"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='头像')
    nickname = models.CharField(max_length=50, blank=True, verbose_name='昵称')
    qq = models.CharField(max_length=20, blank=True, verbose_name='QQ')
    wechat = models.CharField(max_length=50, blank=True, verbose_name='微信')
    bio = models.TextField(blank=True, verbose_name='个人简介')
    
    # 背景设置
    header_bg_type = models.CharField(
        max_length=10,
        choices=[('color', '纯色'), ('image', '图片')],
        default='color',
        verbose_name='背景类型'
    )
    header_bg_color = models.CharField(
        max_length=7,
        default='#808080',
        verbose_name='背景颜色'
    )
    header_bg_image = models.ImageField(
        upload_to='header_bg/',
        null=True,
        blank=True,
        verbose_name='背景图片'
    )
    
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'
    
    def __str__(self):
        return f'{self.user.username}的资料'
    
    def get_display_name(self):
        """获取显示名称，优先使用昵称"""
        return self.nickname if self.nickname else self.user.username
    
    def get_avatar_url(self):
        """获取头像URL，如果没有上传头像则返回默认头像"""
        if self.avatar:
            return self.avatar.url
        else:
            return '/static/images/DefaultProfile_256.png'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """创建用户时自动创建对应的Profile"""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """保存用户时自动保存对应的Profile"""
    instance.profile.save()

class Item(models.Model):
    """物品模型"""
    STATUS_CHOICES = [
        ('available', '在售'),
        ('sold', '已售出'),
        ('reserved', '已预订'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='物品标题')
    description = models.TextField(verbose_name='物品描述')
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='价格')
    image = models.ImageField(upload_to='items/', null=True, blank=True, verbose_name='物品图片')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name='状态')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items', verbose_name='卖家')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '物品'
        verbose_name_plural = '物品'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

class Review(models.Model):
    """评价模型"""
    RATING_CHOICES = [
        (1, '★☆☆☆☆'),
        (2, '★★☆☆☆'),
        (3, '★★★☆☆'),
        (4, '★★★★☆'),
        (5, '★★★★★'),
    ]
    
    content = models.TextField(verbose_name='评价内容')
    rating = models.IntegerField(choices=RATING_CHOICES, default=5, verbose_name='评分')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_reviews', verbose_name='评价人')
    reviewed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_reviews', verbose_name='被评价人')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True, related_name='reviews', verbose_name='关联物品')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='评价时间')
    
    class Meta:
        verbose_name = '评价'
        verbose_name_plural = '评价'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.reviewer.username}对{self.reviewed_user.username}的评价'
    
    def get_rating_display(self):
        """获取评分显示"""
        return dict(self.RATING_CHOICES).get(self.rating, '未知')