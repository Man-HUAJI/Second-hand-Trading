from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # 认证相关
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # 用户个人页面
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/<str:username>/', views.user_profile, name='user_profile'),
    
    # 物品和评价管理
    path('item/create/', views.create_item, name='create_item'),
    path('review/create/<int:user_id>/', views.create_review, name='create_review'),
]