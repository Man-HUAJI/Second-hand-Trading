import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Item

# 删除所有物品数据
items_count = Item.objects.count()
print(f'删除前物品数量: {items_count}')

if items_count > 0:
    Item.objects.all().delete()
    print(f'成功删除 {items_count} 个物品')
else:
    print('数据库中没有物品数据')

# 验证删除结果
remaining_count = Item.objects.count()
print(f'删除后物品数量: {remaining_count}')