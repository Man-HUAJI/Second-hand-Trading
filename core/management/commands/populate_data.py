from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Category, Item
from django.utils.text import slugify
import uuid

class Command(BaseCommand):
    help = 'Populate database with sample categories and items'

    def handle(self, *args, **options):
        # 创建测试用户（如果不存在）
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(self.style.SUCCESS('创建测试用户'))

        # 清空现有数据（可选，用于重新填充）
        Category.objects.all().delete()
        Item.objects.all().delete()
        self.stdout.write(self.style.WARNING('清空现有数据'))

        # 创建分类
        categories_data = [
            {'name': '书籍'},
            {'name': '电子产品'},
            {'name': '生活用品'},
            {'name': '衣物'},
            {'name': '其他'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            # 手动创建分类，确保slug唯一
            base_slug = slugify(cat_data['name'])
            slug = base_slug
            counter = 1
            
            # 检查slug是否已存在
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{uuid.uuid4().hex[:4]}"
                counter += 1
            
            category = Category.objects.create(
                name=cat_data['name'],
                slug=slug
            )
            categories[cat_data['name']] = category
            self.stdout.write(self.style.SUCCESS(f'创建分类: {cat_data["name"]}'))

        # 创建示例物品
        items_data = [
            {
                'title': 'Python编程从入门到实践',
                'description': '几乎全新的Python编程书籍，适合初学者',
                'category': '书籍',
                'price': '25.00',
                'seller': user
            },
            {
                'title': 'iPhone 12 Pro',
                'description': '国行iPhone 12 Pro，256G，功能完好',
                'category': '电子产品',
                'price': '2800.00',
                'seller': user
            },
            {
                'title': '保温杯',
                'description': '不锈钢保温杯，保温效果良好',
                'category': '生活用品',
                'price': '15.00',
                'seller': user
            },
            {
                'title': '冬季羽绒服',
                'description': '品牌羽绒服，L码，只穿过几次',
                'category': '衣物',
                'price': '120.00',
                'seller': user
            },
            {
                'title': '吉他',
                'description': '民谣吉他，适合初学者练习',
                'category': '其他',
                'price': '150.00',
                'seller': user
            },
            {
                'title': '数据结构与算法',
                'description': '计算机专业教材，内容完整',
                'category': '书籍',
                'price': '18.00',
                'seller': user
            },
            {
                'title': '无线耳机',
                'description': '蓝牙无线耳机，音质清晰',
                'category': '电子产品',
                'price': '80.00',
                'seller': user
            },
            {
                'title': '台灯',
                'description': 'LED护眼台灯，亮度可调节',
                'category': '生活用品',
                'price': '25.00',
                'seller': user
            }
        ]

        for item_data in items_data:
            item = Item.objects.create(
                title=item_data['title'],
                description=item_data['description'],
                category=categories[item_data['category']],
                price=item_data['price'],
                seller=item_data['seller']
            )
            self.stdout.write(self.style.SUCCESS(f'创建物品: {item_data["title"]}'))

        self.stdout.write(self.style.SUCCESS('数据填充完成！'))