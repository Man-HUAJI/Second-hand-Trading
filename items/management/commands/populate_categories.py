from django.core.management.base import BaseCommand
from items.models import Category


class Command(BaseCommand):
    help = '添加初始分类数据'
    
    def handle(self, *args, **options):
        # 初始分类数据
        categories = [
            '电子产品',
            '书籍教材', 
            '生活用品',
            '衣物鞋帽',
            '其他物品'
        ]
        
        created_count = 0
        
        for category_name in categories:
            # 检查分类是否已存在
            category, created = Category.objects.get_or_create(
                name=category_name,
                defaults={'name': category_name}
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'成功创建分类: {category_name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'分类已存在: {category_name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'完成！共创建了 {created_count} 个新分类')
        )