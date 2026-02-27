# Users应用AI扩展指南

## 概述
本文档为AI助手提供users应用的架构说明和扩展指导，帮助AI理解现有代码结构并为后续功能扩展提供支持。

## 应用架构

### 核心模型 (models.py)

#### Profile模型
- **功能**：扩展Django内置User模型，存储用户个性化信息
- **关键字段**：
  - `user`：一对一关联Django User
  - `avatar`：用户头像（ImageField）
  - `bio`：个人简介
  - `qq`：QQ联系方式
  - `header_bg_type`：头部背景类型（color/image）
  - `header_bg_color`：纯色背景颜色
  - `header_bg_image`：图片背景

#### Item模型
- **功能**：用户发布的物品
- **关键字段**：
  - `user`：发布者
  - `title`：物品标题
  - `description`：物品描述
  - `price`：价格
  - `category`：分类
  - `image`：物品图片
  - `created_at`：创建时间

#### Review模型
- **功能**：用户收到的评价
- **关键字段**：
  - `user`：被评价用户
  - `reviewer`：评价者
  - `rating`：评分（1-5）
  - `comment`：评价内容
  - `created_at`：创建时间

### 表单系统 (forms.py)

#### UserRegisterForm
- **功能**：用户注册表单
- **字段**：username, email, password1, password2
- **验证**：密码强度、用户名唯一性

#### UserLoginForm
- **功能**：用户登录表单
- **字段**：username, password
- **验证**：用户认证

#### ProfileForm
- **功能**：用户资料编辑表单
- **字段**：所有Profile模型字段
- **特殊处理**：头像和背景图片上传

### 视图系统 (views.py)

#### 认证相关视图
- `register`：用户注册
- `login_view`：用户登录（重定向到首页）
- `logout_view`：用户登出

#### 用户资料视图
- `dashboard`：用户个人主页
- `edit_profile`：编辑用户资料

### URL配置 (urls.py)
- `/register/`：用户注册
- `/login/`：用户登录
- `/logout/`：用户登出
- `/dashboard/`：个人主页
- `/edit/`：编辑资料

## 前端模板结构

### 模板位置
- `templates/users/register.html`：注册页面
- `templates/users/login.html`：登录页面
- `templates/users/dashboard.html`：个人主页

### 关键功能组件

#### 用户信息头部
- **位置**：dashboard.html中的profile-header
- **功能**：显示用户头像、昵称、联系方式
- **背景支持**：纯色背景、图片背景
- **响应式设计**：Bootstrap 5网格系统

#### 图片编辑系统
- **功能**：头像和背景图片裁剪编辑
- **技术**：HTML5 Canvas + JavaScript
- **特性**：
  - 缩放控制（0.01精度）
  - 鼠标拖动
  - 辅助线显示
  - 实时预览
  - 圆形/矩形裁剪

#### 表单交互
- **文件上传**：简化显示，隐藏默认文件输入样式
- **Toast通知**：优雅的操作反馈
- **标签页导航**：个人信息、我的物品、收到的评价

## 扩展指导

### 添加新用户字段
1. 在Profile模型中添加字段
2. 更新ProfileForm表单
3. 修改dashboard.html模板显示
4. 创建数据库迁移

### 添加新功能模块
1. 在models.py中定义新模型
2. 创建对应的表单（如果需要）
3. 在views.py中添加视图函数
4. 配置URL路由
5. 创建模板文件

### 图片处理扩展
- **当前支持**：头像（圆形）、背景（矩形）裁剪
- **扩展方向**：
  - 多尺寸裁剪
  - 滤镜效果
  - 批量处理
  - 图片压缩优化

### 认证系统扩展
- **当前功能**：基础用户名密码认证
- **扩展方向**：
  - 第三方登录（OAuth）
  - 双因素认证
  - 密码重置流程优化
  - 会话管理

## 代码规范

### 命名约定
- 模型类：PascalCase（如Profile, Item）
- 视图函数：snake_case（如register, login_view）
- 模板文件：snake_case.html
- URL模式：kebab-case

### 模板继承
- 使用Django模板继承机制
- 保持一致的页面布局
- 复用公共组件

### 静态资源
- CSS/JavaScript：使用Bootstrap 5
- 图片：存储在static/images目录
- 用户上传：存储在media目录

## 数据库关系

```
User (Django内置)
  └── Profile (一对一)
        ├── Item (一对多)
        └── Review (一对多，作为被评价者)
```

## 安全考虑

### 已实现
- 密码哈希存储
- CSRF保护
- 文件上传类型限制
- XSS防护（模板自动转义）

### 建议扩展
- 文件上传大小限制
- 图片格式验证
- 会话安全增强
- 权限控制细化

## 性能优化建议

### 数据库优化
- 为常用查询字段添加索引
- 使用select_related/prefetch_related减少查询
- 考虑分页显示大量数据

### 前端优化
- 图片懒加载
- JavaScript代码压缩
- CSS优化

## 测试指导

### 单元测试
- 模型方法测试
- 表单验证测试
- 视图逻辑测试

### 集成测试
- 用户注册流程
- 登录认证流程
- 图片上传处理

## 部署注意事项

### 静态文件
- 配置STATIC_ROOT和STATIC_URL
- 配置MEDIA_ROOT和MEDIA_URL
- 生产环境使用CDN

### 环境配置
- 设置DEBUG=False
- 配置ALLOWED_HOSTS
- 设置SECRET_KEY

## 故障排除

### 常见问题
1. **图片无法显示**：检查MEDIA_URL配置
2. **模板渲染错误**：检查模板语法和变量传递
3. **表单验证失败**：检查表单字段定义

### 调试方法
- 使用Django调试工具栏
- 查看服务器日志
- 检查浏览器开发者工具

## 版本兼容性

- **Django版本**：4.2.28
- **Python版本**：3.9+
- **Bootstrap版本**：5.x

---

*本文档最后更新：2026-02-27*
*维护者：AI助手*