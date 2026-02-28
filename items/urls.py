from django.urls import path
from . import views

urlpatterns = [
    # 首页
    path('', views.home, name='home'),
    
    # 物品相关
    path('create/', views.item_create, name='item_create'),
    path('<int:pk>/', views.item_detail, name='item_detail'),
    path('<int:pk>/edit/', views.item_edit, name='item_edit'),
    path('<int:pk>/toggle/', views.item_toggle_status, name='item_toggle_status'),
    
    # 列表和搜索
    path('list/', views.item_list, name='item_list'),
    path('my/', views.my_items, name='my_items'),
]