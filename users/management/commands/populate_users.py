from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Profile, Item, Review
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate database with sample users, items, and reviews'

    def handle(self, *args, **options):
        # 创建测试用户
        users_data = [
            {
                'username': '张三',
                'email': 'zhangsan@example.com',
                'password': 'password123',
                'nickname': '张三同学',
                'qq': '123456789',
                'wechat': 'zhangsan123',
                'bio': '热爱学习，喜欢分享的计算机专业学生'
            },
            {
                'username': '李四',
                'email': 'lisi@example.com',
                'password': 'password123',
                'nickname': '李四学长',
                'qq': '987654321',
                'wechat': 'lisi456',
                'bio': '即将毕业的大四学长，有很多闲置物品'
            },
            {
                'username': '王五',
                'email': 'wangwu@example.com',
                'password': 'password123',
                'nickname': '王五学姐',
                'qq': '555555555',
                'wechat': 'wangwu789',
                'bio': '文学院学姐，喜欢阅读和写作'
            }
        ]
        
        created_users = {}
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['nickname'].replace('同学', '').replace('学长', '').replace('学姐', '').strip()
                }
            )
            
            if created:
                user.set_password(user_data['password'])
                user.save()
                
                # 更新用户资料
                profile = user.profile
                profile.nickname = user_data['nickname']
                profile.qq = user_data['qq']
                profile.wechat = user_data['wechat']
                profile.bio = user_data['bio']
                profile.save()
                
                created_users[user_data['username']] = user
                self.stdout.write(self.style.SUCCESS(f'创建用户: {user_data["username"]}'))
            else:
                created_users[user_data['username']] = user

        # 创建示例物品
        items_data = [
            {
                'title': 'Python编程从入门到实践',
                'description': '几乎全新的Python编程书籍，适合初学者学习编程基础',
                'price': '25.00',
                'status': 'available',
                'seller': '张三'
            },
            {
                'title': 'iPhone 12 Pro',
                'description': '国行iPhone 12 Pro，256G，功能完好，保护得很好',
                'price': '2800.00',
                'status': 'available',
                'seller': '张三'
            },
            {
                'title': '保温杯',
                'description': '不锈钢保温杯，保温效果良好，适合上课使用',
                'price': '15.00',
                'status': 'sold',
                'seller': '李四'
            },
            {
                'title': '冬季羽绒服',
                'description': '品牌羽绒服，L码，只穿过几次，保暖效果好',
                'price': '120.00',
                'status': 'available',
                'seller': '李四'
            },
            {
                'title': '文学理论教程',
                'description': '文学院教材，内容完整，有少量笔记',
                'price': '18.00',
                'status': 'available',
                'seller': '王五'
            },
            {
                'title': '无线耳机',
                'description': '蓝牙无线耳机，音质清晰，续航时间长',
                'price': '80.00',
                'status': 'reserved',
                'seller': '王五'
            }
        ]

        created_items = {}
        for item_data in items_data:
            item, created = Item.objects.get_or_create(
                title=item_data['title'],
                defaults={
                    'description': item_data['description'],
                    'price': item_data['price'],
                    'status': item_data['status'],
                    'seller': created_users[item_data['seller']]
                }
            )
            
            if created:
                created_items[item_data['title']] = item
                self.stdout.write(self.style.SUCCESS(f'创建物品: {item_data["title"]}'))

        # 创建示例评价
        reviews_data = [
            {
                'content': '交易很顺利，物品质量很好，卖家很靠谱！',
                'rating': 5,
                'reviewer': '李四',
                'reviewed_user': '张三',
                'item': 'Python编程从入门到实践'
            },
            {
                'content': '卖家很耐心，物品描述准确，推荐！',
                'rating': 4,
                'reviewer': '王五',
                'reviewed_user': '张三',
                'item': 'iPhone 12 Pro'
            },
            {
                'content': '交易过程很愉快，物品性价比高',
                'rating': 5,
                'reviewer': '张三',
                'reviewed_user': '李四',
                'item': '保温杯'
            },
            {
                'content': '卖家服务态度很好，物品质量不错',
                'rating': 4,
                'reviewer': '王五',
                'reviewed_user': '李四',
                'item': '冬季羽绒服'
            },
            {
                'content': '书籍保存得很好，价格实惠',
                'rating': 5,
                'reviewer': '张三',
                'reviewed_user': '王五',
                'item': '文学理论教程'
            },
            {
                'content': '耳机音质不错，卖家很专业',
                'rating': 4,
                'reviewer': '李四',
                'reviewed_user': '王五',
                'item': '无线耳机'
            }
        ]

        for review_data in reviews_data:
            review, created = Review.objects.get_or_create(
                reviewer=created_users[review_data['reviewer']],
                reviewed_user=created_users[review_data['reviewed_user']],
                item=created_items.get(review_data['item']),
                defaults={
                    'content': review_data['content'],
                    'rating': review_data['rating']
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'创建评价: {review_data["reviewer"]} -> {review_data["reviewed_user"]}'))

        self.stdout.write(self.style.SUCCESS('用户系统数据填充完成！'))
        self.stdout.write(self.style.SUCCESS('测试账号信息：'))
        self.stdout.write(self.style.SUCCESS('用户名: 张三, 密码: password123'))
        self.stdout.write(self.style.SUCCESS('用户名: 李四, 密码: password123'))
        self.stdout.write(self.style.SUCCESS('用户名: 王五, 密码: password123'))