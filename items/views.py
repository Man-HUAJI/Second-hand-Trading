from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Item, Category
from .forms import ItemForm


def home(request):
    """首页视图，显示最新发布的物品"""
    # 获取最新的6个在售物品
    latest_items = Item.objects.filter(status='active').order_by('-created_at')[:6]
    
    # 获取所有分类
    categories = Category.objects.all()
    
    context = {
        'latest_items': latest_items,
        'categories': categories,
    }
    
    return render(request, 'core/mainpage.html', context)


@login_required
def item_create(request):
    """发布物品视图"""
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            # 创建物品但不立即保存
            item = form.save(commit=False)
            # 设置发布者为当前登录用户
            item.seller = request.user
            # 保存物品
            item.save()
            
            messages.success(request, '物品发布成功！')
            # 重定向到物品详情页
            return redirect(item.get_absolute_url())
        else:
            messages.error(request, '发布失败，请检查表单信息')
    else:
        form = ItemForm()
    
    context = {
        'form': form,
        'title': '发布物品'
    }
    
    return render(request, 'items/item_form.html', context)


def item_detail(request, pk):
    """物品详情视图"""
    # 获取物品，如果不存在则返回404
    item = get_object_or_404(Item, pk=pk)
    
    # 检查当前用户是否为物品发布者
    is_owner = request.user.is_authenticated and item.seller == request.user
    
    context = {
        'item': item,
        'is_owner': is_owner,
    }
    
    return render(request, 'items/item_detail.html', context)


def item_list(request):
    """物品列表视图（可选功能）"""
    items = Item.objects.filter(status='active').order_by('-created_at')
    
    # 搜索功能
    query = request.GET.get('q')
    if query:
        items = items.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query)
        )
    
    # 分类筛选
    category_id = request.GET.get('category')
    if category_id:
        items = items.filter(category_id=category_id)
    
    categories = Category.objects.all()
    
    context = {
        'items': items,
        'categories': categories,
        'query': query or '',
        'selected_category': int(category_id) if category_id else None,
    }
    
    return render(request, 'items/item_list.html', context)


@login_required
def my_items(request):
    """我的物品视图"""
    items = Item.objects.filter(seller=request.user).order_by('-created_at')
    
    context = {
        'items': items,
    }
    
    return render(request, 'items/my_items.html', context)


@login_required
def item_edit(request, pk):
    """编辑物品视图（可选功能）"""
    item = get_object_or_404(Item, pk=pk, seller=request.user)
    
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, '物品信息更新成功！')
            return redirect(item.get_absolute_url())
        else:
            messages.error(request, '更新失败，请检查表单信息')
    else:
        form = ItemForm(instance=item)
    
    context = {
        'form': form,
        'title': '编辑物品',
        'item': item,
    }
    
    return render(request, 'items/item_form.html', context)


@login_required
def item_toggle_status(request, pk):
    """切换物品状态（上架/下架）"""
    item = get_object_or_404(Item, pk=pk, seller=request.user)
    
    if item.status == 'active':
        item.status = 'inactive'
        message = '物品已下架'
    else:
        item.status = 'active'
        message = '物品已上架'
    
    item.save()
    messages.success(request, message)
    
    return redirect('my_items')