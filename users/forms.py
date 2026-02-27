from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile, Item, Review

class CustomUserCreationForm(UserCreationForm):
    """自定义用户注册表单"""
    email = forms.EmailField(
        required=False,
        label='邮箱',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入邮箱地址（可选）',
            'style': 'user-select: text; -webkit-user-select: text; -moz-user-select: text; -ms-user-select: text;'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': '用户名',
            'password1': '密码',
            'password2': '确认密码',
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入用户名',
                'style': 'user-select: text; -webkit-user-select: text; -moz-user-select: text; -ms-user-select: text;'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入密码',
                'style': 'user-select: text; -webkit-user-select: text; -moz-user-select: text; -ms-user-select: text;'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': '请再次输入密码',
                'style': 'user-select: text; -webkit-user-select: text; -moz-user-select: text; -ms-user-select: text;'
            }),
        }
    
    def clean_username(self):
        """验证用户名唯一性"""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError('该用户名已被注册，请选择其他用户名')
        return username
    
    def clean_email(self):
        """验证邮箱唯一性"""
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError('该邮箱已被注册，请使用其他邮箱')
        return email
    
    def clean_password2(self):
        """验证密码一致性"""
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError('两次输入的密码不一致')
        
        # 密码强度验证
        if len(password1) < 8:
            raise ValidationError('密码长度至少为8个字符')
        
        return password2

class CustomAuthenticationForm(AuthenticationForm):
    """自定义登录表单"""
    username = forms.CharField(
        label='用户名或邮箱',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入用户名或邮箱',
            'style': 'user-select: text; -webkit-user-select: text; -moz-user-select: text; -ms-user-select: text;'
        })
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入密码',
            'style': 'user-select: text; -webkit-user-select: text; -moz-user-select: text; -ms-user-select: text;'
        })
    )
    
    def clean_username(self):
        """支持用户名或邮箱登录"""
        username = self.cleaned_data.get('username')
        if '@' in username:
            # 如果是邮箱格式，查找对应的用户名
            try:
                user = User.objects.get(email=username)
                return user.username
            except User.DoesNotExist:
                raise ValidationError('该邮箱未注册')
        return username

class ProfileUpdateForm(forms.ModelForm):
    """用户资料更新表单"""
    class Meta:
        model = Profile
        fields = ['nickname', 'avatar', 'qq', 'wechat', 'bio', 'header_bg_type', 'header_bg_color', 'header_bg_image']
        labels = {
            'nickname': '昵称',
            'avatar': '头像',
            'qq': 'QQ',
            'wechat': '微信',
            'bio': '个人简介',
        }
        widgets = {
            'nickname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入昵称',
                'style': 'user-select: text; -webkit-user-select: text; -moz-user-select: text; -ms-user-select: text;'
            }),
            'qq': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入QQ号',
                'style': 'user-select: text; -webkit-user-select: text; -moz-user-select: text; -ms-user-select: text;'
            }),
            'wechat': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入微信号',
                'style': 'user-select: text; -webkit-user-select: text; -moz-user-select: text; -ms-user-select: text;'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '请输入个人简介',
                'rows': 4,
                'style': 'user-select: text; -webkit-user-select: text; -moz-user-select: text; -ms-user-select: text;'
            }),
            'header_bg_color': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入十六进制颜色代码',
                'style': 'user-select: text; -webkit-user-select: text; -moz-user-select: text; -ms-user-select: text;'
            }),
        }

class ItemForm(forms.ModelForm):
    """物品发布表单"""
    class Meta:
        model = Item
        fields = ['title', 'description', 'price', 'image', 'status']
        labels = {
            'title': '物品标题',
            'description': '物品描述',
            'price': '价格',
            'image': '物品图片',
            'status': '状态',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入物品标题'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '请输入物品描述',
                'rows': 4
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入价格',
                'step': '0.01'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

class ReviewForm(forms.ModelForm):
    """评价表单"""
    class Meta:
        model = Review
        fields = ['content', 'rating']
        labels = {
            'content': '评价内容',
            'rating': '评分',
        }
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '请输入评价内容',
                'rows': 3
            }),
            'rating': forms.Select(attrs={
                'class': 'form-select'
            }),
        }