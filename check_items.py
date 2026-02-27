import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Item

print('物品数量:', Item.objects.count())
if Item.objects.exists():
    print('最新物品:')
    for item in Item.objects.all()[:3]:
        print(f'  - {item.title} ({item.created_at})')
else:
    print('数据库中没有物品')