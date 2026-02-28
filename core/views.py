from django.shortcuts import render
from .models import Category

def home(request):
    # 获取所有分类
    categories = Category.objects.all()
    
    context = {
        'categories': categories,
    }
    
    return render(request, 'core/mainpage.html', context)