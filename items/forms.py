from django import forms
from .models import Item, Category


class ItemForm(forms.ModelForm):
    """物品发布表单"""
    
    class Meta:
        model = Item
        fields = [
            'title', 'category', 'description', 'price', 'trade_method', 
            'contact', 'condition', 'image'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入物品标题'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': '请详细描述物品信息，如品牌、型号、使用情况等',
                'rows': 5
            }),
            'price': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '例如：100 或 50-100（单位：元）'
            }),
            'trade_method': forms.Select(attrs={
                'class': 'form-select'
            }),
            'contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '请输入联系方式（如微信号、手机号）'
            }),
            'condition': forms.Select(attrs={
                'class': 'form-select'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        labels = {
            'title': '物品标题',
            'category': '物品分类',
            'description': '详细描述',
            'trade_method': '交易方式',
            'contact': '联系方式',
            'condition': '物品状态',
            'image': '物品图片'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 设置分类字段的查询集，只显示活跃的分类
        self.fields['category'].queryset = Category.objects.all()
        
        # 为必填字段添加星号标记
        self.fields['title'].label += ' *'
        self.fields['category'].label += ' *'
        self.fields['description'].label += ' *'
        self.fields['contact'].label += ' *'
    
    def clean_title(self):
        """验证物品标题"""
        title = self.cleaned_data.get('title')
        if len(title.strip()) < 2:
            raise forms.ValidationError('物品标题太短，请至少输入2个字符')
        if len(title) > 200:
            raise forms.ValidationError('物品标题过长，请控制在200个字符以内')
        return title.strip()
    
    def clean_description(self):
        """验证物品描述"""
        description = self.cleaned_data.get('description')
        if len(description.strip()) < 10:
            raise forms.ValidationError('物品描述太短，请至少输入10个字符')
        return description.strip()
    
    def clean_contact(self):
        """验证联系方式"""
        contact = self.cleaned_data.get('contact')
        if len(contact.strip()) < 2:
            raise forms.ValidationError('联系方式太短，请至少输入2个字符')
        return contact.strip()
    
    def clean_image(self):
        """验证图片文件"""
        image = self.cleaned_data.get('image')
        if image:
            # 检查文件大小（限制为5MB）
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError('图片文件太大，请上传小于5MB的图片')
            
            # 检查文件类型
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
            if not any(image.name.lower().endswith(ext) for ext in valid_extensions):
                raise forms.ValidationError('不支持的文件格式，请上传图片文件（JPG、PNG、GIF、WebP）')
        
        return image