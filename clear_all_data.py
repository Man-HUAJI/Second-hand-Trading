#!/usr/bin/env python
"""
清理所有用户数据和物品数据脚本
保留管理员账户（username为'admin'的用户）
"""

import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from items.models import Item
from users.models import Profile, Review

def clear_all_data():
    """清理所有用户数据和物品数据，保留管理员账户"""
    
    print("=" * 50)
    print("开始清理数据库数据...")
    print("=" * 50)
    
    # 统计删除前的数据量
    users_count = User.objects.count()
    items_count = Item.objects.count()
    profiles_count = Profile.objects.count()
    reviews_count = Review.objects.count()
    
    print(f"删除前数据统计:")
    print(f"  用户数量: {users_count}")
    print(f"  物品数量: {items_count}")
    print(f"  用户资料数量: {profiles_count}")
    print(f"  评价数量: {reviews_count}")
    print("-" * 50)
    
    # 删除所有物品数据
    if items_count > 0:
        deleted_items = Item.objects.all().delete()
        print(f"✓ 成功删除 {deleted_items[0]} 个物品")
    else:
        print("✓ 数据库中没有物品数据")
    
    # 删除所有评价数据
    if reviews_count > 0:
        deleted_reviews = Review.objects.all().delete()
        print(f"✓ 成功删除 {deleted_reviews[0]} 条评价")
    else:
        print("✓ 数据库中没有评价数据")
    
    # 删除非管理员用户及其资料
    admin_users = User.objects.filter(username='admin')
    if admin_users.exists():
        # 保留管理员账户
        users_to_delete = User.objects.exclude(username='admin')
        profiles_to_delete = Profile.objects.exclude(user__username='admin')
        
        deleted_users_count = users_to_delete.count()
        deleted_profiles_count = profiles_to_delete.count()
        
        if deleted_users_count > 0:
            deleted_users = users_to_delete.delete()
            print(f"✓ 成功删除 {deleted_users_count} 个非管理员用户")
        else:
            print("✓ 数据库中没有非管理员用户")
            
        if deleted_profiles_count > 0:
            deleted_profiles = profiles_to_delete.delete()
            print(f"✓ 成功删除 {deleted_profiles_count} 个非管理员用户资料")
        else:
            print("✓ 数据库中没有非管理员用户资料")
            
        # 显示保留的管理员信息
        admin_user = admin_users.first()
        print(f"✓ 保留管理员账户: {admin_user.username} (ID: {admin_user.id})")
    else:
        # 如果没有管理员账户，删除所有用户
        deleted_users = User.objects.all().delete()
        deleted_profiles = Profile.objects.all().delete()
        print(f"✓ 成功删除所有用户数据（共 {deleted_users[0]} 个用户）")
        print("⚠ 注意：系统中没有管理员账户")
    
    print("-" * 50)
    
    # 统计删除后的数据量
    remaining_users = User.objects.count()
    remaining_items = Item.objects.count()
    remaining_profiles = Profile.objects.count()
    remaining_reviews = Review.objects.count()
    
    print(f"删除后数据统计:")
    print(f"  用户数量: {remaining_users}")
    print(f"  物品数量: {remaining_items}")
    print(f"  用户资料数量: {remaining_profiles}")
    print(f"  评价数量: {remaining_reviews}")
    print("=" * 50)
    
    # 验证清理结果
    if remaining_items == 0 and remaining_reviews == 0:
        print("✅ 数据清理完成！")
        
        if remaining_users == 1 and User.objects.filter(username='admin').exists():
            print("✅ 管理员账户已保留")
        elif remaining_users == 0:
            print("⚠ 所有用户数据已删除，包括管理员")
        else:
            print(f"⚠ 剩余 {remaining_users} 个用户，请检查是否需要进一步清理")
    else:
        print("❌ 数据清理可能不完整，请检查")

if __name__ == "__main__":
    # 确认操作
    print("警告：此操作将删除所有用户数据和物品数据！")
    print("仅保留管理员账户（username为'admin'的用户）")
    
    confirm = input("确认执行数据清理操作？(输入 'YES' 确认): ")
    
    if confirm == "YES":
        clear_all_data()
    else:
        print("操作已取消")