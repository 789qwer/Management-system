# 智慧图书馆管理系统

基于 Django + Bootstrap 的一站式智慧图书馆管理平台，集成自习室预约、图书借阅、饮品吧服务三大模块。

## 功能概览

### 学生端
- **自习室预约**：按楼层浏览阅览空间，飞机舱位风格平面图选座，支持签到/签退/取消
- **图书借阅**：检索图书（书名/作者/ISBN/分类），在线借阅、续借、归还
- **饮品吧**：咖啡/茶饮/果汁/小食下单，可选甜度与温度，生成取餐码
- **个人中心**：查看预约记录、学习时长、违规记录、借阅与订单

### 管理后台
- **仪表盘**：开放空间、可用座位、馆藏图书、今日订单等统计
- **用户管理**：增删改查、重置密码、角色分配
- **空间与座位**：阅览空间 CRUD、自定义座位布局（坐标定位）
- **预约记录**：查看/删除预约
- **违规管理**：爽约记录与信用分管理
- **图书管理**：图书 CRUD、借阅记录
- **饮品管理**：饮品 CRUD、订单处理（出餐标记）

## 技术栈

| 类别 | 选型 |
|------|------|
| 后端 | Python 3.x + Django 5.x |
| 前端 | Bootstrap 5 + Bootstrap Icons |
| 数据库 | SQLite（开发） |
| 认证 | Django 内置 Auth（自定义 User 模型） |

## 项目结构

```
Campus Study Room Check-In Management System/
├── manage.py
├── requirements.txt
├── studyroom_system/          # Django 项目配置
│   ├── settings.py
│   └── urls.py
└── studyroom/                 # 主应用
    ├── models.py              # 数据模型
    ├── views.py               # 视图逻辑
    ├── urls.py                # 路由
    ├── forms.py               # 表单
    ├── admin.py               # Admin 注册
    ├── migrations/            # 数据库迁移
    └── templates/studyroom/   # 模板
        ├── base.html          # 学生端模板
        ├── base_admin.html    # 管理端模板
        ├── home.html          # 首页
        ├── room_list.html     # 空间列表
        ├── room_detail.html   # 选座平面图
        ├── books.html         # 图书列表
        ├── book_detail.html   # 图书详情
        ├── my_borrows.html    # 我的借阅
        ├── cafe.html          # 饮品吧
        ├── my_orders.html     # 我的订单
        ├── profile.html       # 个人中心
        ├── login.html / register.html
        └── ...
```

## 快速开始

### 1. 环境要求

- Python 3.10+
- 虚拟环境（项目已自带 `venv`）

### 2. 启动服务

Windows CMD：

```cmd
cd "c:\Users\yuxingjia\Desktop\Campus Study Room Check-In Management System"
venv\Scripts\python.exe manage.py runserver
```

PowerShell：

```powershell
cd "c:\Users\yuxingjia\Desktop\Campus Study Room Check-In Management System"; venv\Scripts\python.exe manage.py runserver
```

启动后访问：http://127.0.0.1:8000/

### 3. 安装依赖（如需）

```bash
venv\Scripts\pip.exe install -r requirements.txt
```

### 4. 数据库迁移（首次或模型变更时）

```bash
venv\Scripts\python.exe manage.py migrate
```

### 5. 默认管理员

| 用户名 | 密码 |
|--------|------|
| `admin` | `Admin123456` |

登录后访问：
- 系统后台：http://127.0.0.1:8000/manage/dashboard/
- Django Admin：http://127.0.0.1:8000/admin/

## 数据模型

### User（用户）
继承 `AbstractUser`，新增 `role`（student/admin）、`student_id`、`credit_score`。

### StudyRoom（阅览空间）
字段：name、floor（楼层）、book_category（图书分类）、capacity、open_time、close_time、status、layout（座位布局 JSON）、shelves（书柜布局 JSON）、description。

### Seat（座位）
字段：room（外键）、seat_no、position_x、position_y（百分比坐标）、status。

### Reservation（预约）
字段：user、seat、date、start_time、end_time、status（pending/checked_in/checked_out/cancelled/no_show）。

### Book / BorrowRecord（图书 / 借阅记录）
- Book：title、author、isbn、category、total_copies、available_copies、location
- BorrowRecord：user、book、borrow_at、due_at、return_at、status、renew_count（续借次数，上限 2 次）

### Drink / DrinkOrder（饮品 / 订单）
- Drink：name、category（coffee/tea/juice/snack）、price、available
- DrinkOrder：user、drink、quantity、sweetness（甜度）、temperature（温度）、pickup_code、status、total_price

## 核心业务规则

- **预约签到窗口**：开始前 15 分钟 ~ 后 30 分钟，超时未签到记为爽约
- **借阅期限**：14 天，可续借 2 次（每次顺延 14 天）
- **并发安全**：借书/还书操作使用 `transaction.atomic()` + `select_for_update()` 行锁，防止超卖
- **唯一性约束**：同一用户不可同时借阅同一本书（数据库层约束）

## 生产部署注意

上线前必须修改 `studyroom_system/settings.py`：

1. `SECRET_KEY` 改为环境变量读取
2. `DEBUG = False`
3. `ALLOWED_HOSTS` 限制为实际域名
4. 配置 `LOGGING` 日志输出
5. 数据库建议切换为 PostgreSQL/MySQL

## 许可

开发演示项目。
