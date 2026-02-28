from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Avg
from items.models import Item  # 使用items应用中的Item模型
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileUpdateForm, ReviewForm
from .models import Profile, Review

def register(request):
    """用户注册视图"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # 自动登录用户
            login(request, user)
            messages.success(request, f'注册成功！欢迎 {user.username}')
            return redirect('users:dashboard')
        else:
            messages.error(request, '注册失败，请检查表单错误')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    """用户登录视图"""
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'登录成功！欢迎 {user.username}')
                
                # 重定向到用户请求的页面或首页
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, '用户名或密码错误')
        else:
            messages.error(request, '登录失败，请检查表单错误')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})

@login_required
def user_logout(request):
    """用户登出视图"""
    logout(request)
    messages.success(request, '您已成功退出登录')
    return redirect('home')

@login_required
def dashboard(request):
    """用户仪表板视图"""
    user = request.user
    profile = user.profile
    
    # 获取用户发布的物品
    user_items = Item.objects.filter(seller=user).order_by('-created_at')
    
    # 获取用户收到的评价
    user_reviews = Review.objects.filter(reviewed_user=user).order_by('-created_at')
    
    # 计算平均评分
    avg_rating = user_reviews.aggregate(Avg('rating'))['rating__avg']
    
    # 获取用户给出的评价
    given_reviews = Review.objects.filter(reviewer=user).order_by('-created_at')
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, '个人信息更新成功！')
            return redirect('users:dashboard')
        else:
            messages.error(request, '更新失败，请检查表单错误')
    else:
        form = ProfileUpdateForm(instance=profile)
    
    context = {
        'profile': profile,
        'form': form,
        'user_items': user_items,
        'user_reviews': user_reviews,
        'given_reviews': given_reviews,
        'avg_rating': avg_rating or 0,
        'review_count': user_reviews.count(),
    }
    
    return render(request, 'users/dashboard.html', context)

@login_required
def create_item(request):
    """创建物品视图"""
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.seller = request.user
            item.save()
            messages.success(request, '物品发布成功！')
            return redirect('users:dashboard')
        else:
            messages.error(request, '发布失败，请检查表单错误')
    else:
        form = ItemForm()
    
    return render(request, 'users/create_item.html', {'form': form})

@login_required
def create_review(request, user_id):
    """创建评价视图"""
    reviewed_user = get_object_or_404(User, id=user_id)
    
    # 不能给自己评价
    if reviewed_user == request.user:
        messages.error(request, '不能给自己评价')
        return redirect('users:dashboard')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.reviewed_user = reviewed_user
            review.save()
            messages.success(request, '评价发布成功！')
            return redirect('users:dashboard')
        else:
            messages.error(request, '评价失败，请检查表单错误')
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'reviewed_user': reviewed_user,
    }
    
    return render(request, 'users/create_review.html', context)

def user_profile(request, username):
    """用户公开资料页面"""
    user = get_object_or_404(User, username=username)
    profile = user.profile
    
    # 获取用户公开的物品（在售状态）
    public_items = Item.objects.filter(seller=user, status='active').order_by('-created_at')
    
    # 获取用户收到的评价
    user_reviews = Review.objects.filter(reviewed_user=user).order_by('-created_at')
    
    # 计算平均评分
    avg_rating = user_reviews.aggregate(Avg('rating'))['rating__avg']
    
    context = {
        'profile_user': user,
        'profile': profile,
        'public_items': public_items,
        'user_reviews': user_reviews,
        'avg_rating': avg_rating or 0,
        'review_count': user_reviews.count(),
    }
    
    return render(request, 'users/user_profile.html', context)