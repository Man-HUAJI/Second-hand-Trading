from django.shortcuts import render
from .models import Category, Item

def home(request):
    # 获取所有分类
    categories = Category.objects.all()
    
    # 获取最新发布的6个物品（按时间倒序）
    latest_items = Item.objects.select_related('category', 'seller').all()[:6]
    
    context = {
        'categories': categories,
        'latest_items': latest_items,
    }
    
    return render(request, 'core/mainpage.html', context)