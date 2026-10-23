# 智慧图书馆管理系统

基于 Django + Bootstrap 的一站式智慧图书馆管理平台，集成自习室预约、图书借阅、饮品吧服务三大模块。

## 功能概览

### 学生端
- **自习室预约**：按楼层浏览阅览空间，平面图选座（书柜/座位百分比坐标），支持签到/签退/取消
- **图书借阅**：检索图书（书名/作者/ISBN/分类），在线借阅、续借、归还
- **饮品吧**：咖啡/茶饮/果汁/小食下单，可选甜度与温度，生成当天唯一取餐码
- **个人中心**：预约记录、学习时长、信用分、违规记录、借阅与订单

### 管理后台
- **数据看板**：开放空间、座位占用率、今日预约、馆藏图书、今日订单、近 7 天趋势
- **用户管理**：增删改查、重置密码、角色分配、信用分维护
- **空间与座位**：阅览空间 CRUD、座位布局自动生成、坐标手工微调、一键重新布局
- **预约记录**：按状态筛选、分页、删除
- **违规管理**：爽约记录与信用分自动扣分/回补
- **图书管理**：图书 CRUD、借阅记录
- **饮品管理**：饮品 CRUD、订单处理（出餐标记）

## 技术栈

| 类别 | 选型 |
|------|------|
| 后端 | Python 3.10+ / Django 5.2 |
| 前端 | Bootstrap 5.3 + Bootstrap Icons（CDN） + 少量原生 JS |
| 样式 | 统一放在 `static/css/`，模板不再内联大段 CSS |
| 数据库 | SQLite（默认，开箱即用） / MySQL 8（部署方案见 `docs/PyCharm+MySQL迁移部署指南.md`） |
| 认证 | Django 内置 Auth（自定义 User 模型 + 角色字段） |

## 项目结构

```
Campus Study Room Check-In Management System/
├── manage.py
├── requirements.txt
├── .env.example               # 环境变量模板（复制为 .env）
├── docs/
│   └── PyCharm+MySQL迁移部署指南.md   # SQLite → MySQL 部署与数据迁移手册
├── data_export/               # export_data 产物（迁移用，已 gitignore）
├── studyroom_system/
│   ├── __init__.py            # mysqlclient / PyMySQL 驱动兜底
│   ├── settings.py            # .env + DB_ENGINE(sqlite|mysql) + 日志 + STATIC_ROOT
│   └── urls.py
├── static/                    # 全站静态资源（由 settings 收集）
│   ├── css/ base.css admin.css landing.css seatmap.css cafe.css
│   └── js/  app.js
└── studyroom/
    ├── models.py              # 数据模型
    ├── services.py            # 业务服务层（座位可用性/布局生成/爽约处理）
    ├── decorators.py          # admin_required（非管理员 403，而不是重定向死循环）
    ├── signals.py             # 违规记录 ⇄ 信用分联动
    ├── forms.py               # 表单与业务校验
    ├── views/                 # 视图按领域拆包
    │   ├── public.py          auth.py
    │   ├── student_rooms.py   student_books.py   student_cafe.py
    │   └── admin_dashboard.py admin_users.py admin_rooms.py
    │       admin_records.py   admin_library.py
    ├── urls.py                # 聚合 public / student / admin 三份路由
    ├── urls_public.py urls_student.py urls_admin.py
    ├── fixtures/rooms.json    # 8 个示例房间配置（seed_data 使用）
    ├── management/commands/   # seed_data / export_data / import_data
    │                          # mark_no_shows / rebuild_seats
    ├── migrations/
    ├── tests/                 # 66 个自动化测试
    └── templates/studyroom/   # 模板
```

## 快速开始

### 1. 环境要求

- Python 3.10+
- 虚拟环境（项目已自带 `venv`）

### 2. 启动服务

PowerShell：

```powershell
cd "c:\Users\yuxingjia\Desktop\Campus Study Room Check-In Management System"
venv\Scripts\python.exe manage.py runserver
```

启动后访问：http://127.0.0.1:8000/

### 3. 安装依赖

```bash
venv\Scripts\pip.exe install -r requirements.txt
```

### 4. 数据库迁移与初始化数据

```bash
venv\Scripts\python.exe manage.py migrate
venv\Scripts\python.exe manage.py seed_data      # 房间 + 座位 + 图书 + 饮品（表为空时写入）
```

### 5. 改用 MySQL

一句话版：复制 `.env.example` 为 `.env`，把 `DB_ENGINE` 改成 `mysql` 并填好 `DB_*`，然后
`pip install mysqlclient` → `migrate`。**已有数据搬迁、建库建号、PyCharm 解释器/运行配置、FAQ**
都在 [`docs/PyCharm+MySQL迁移部署指南.md`](docs/PyCharm+MySQL迁移部署指南.md) 里。

```powershell
# 旧库导出 → 换库 → 建表 → 导入
venv\Scripts\python.exe manage.py export_data
venv\Scripts\python.exe manage.py migrate
venv\Scripts\python.exe manage.py import_data
```

### 6. 默认管理员

| 用户名 | 密码 |
|--------|------|
| `admin` | `Admin123456` |

登录后访问：
- 系统后台：http://127.0.0.1:8000/manage/dashboard/
- Django Admin：http://127.0.0.1:8000/admin/

## 常用运维命令

```bash
# 爽约与超时预约处理（建议每 10 分钟跑一次，配合系统计划任务）
venv\Scripts\python.exe manage.py mark_no_shows
venv\Scripts\python.exe manage.py mark_no_shows --dry-run   # 只统计不写库

# 按容量/布局重算座位坐标，并补齐或清理座位
venv\Scripts\python.exe manage.py rebuild_seats
venv\Scripts\python.exe manage.py rebuild_seats --room 6

# 数据导出 / 导入（SQLite ⇄ MySQL 迁移）
venv\Scripts\python.exe manage.py export_data                 # → data_export/*.json
venv\Scripts\python.exe manage.py import_data                 # 追加导入
venv\Scripts\python.exe manage.py import_data --fresh         # 清空后导入

# 运行测试
venv\Scripts\python.exe manage.py test studyroom

# 生产静态文件
venv\Scripts\python.exe manage.py collectstatic
```

Windows 计划任务示例（每 10 分钟）：

```
程序：   <项目路径>\venv\Scripts\python.exe
参数：   manage.py mark_no_shows
起始于： <项目路径>
```

## 环境变量

配置优先级：真实环境变量 > 项目根 `.env` > `settings.py` 默认值。模板见 `.env.example`。

| 变量 | 说明 | 默认 |
|------|------|------|
| `DJANGO_SECRET_KEY` | 密钥，生产必改 | `dev-insecure-change-me-in-production` |
| `DJANGO_DEBUG` | `0` / `1` | `1` |
| `DJANGO_ALLOWED_HOSTS` | 逗号分隔域名 | `*` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | 逗号分隔，HTTPS 部署需要 | 空 |
| `DJANGO_TIME_ZONE` | 时区 | `Asia/Shanghai` |
| `DJANGO_SECURE_COOKIES` | `DEBUG=0` 时是否启用 Secure Cookie | `1` |
| `DJANGO_SECURE_SSL_REDIRECT` | `DEBUG=0` 时是否强制 HTTPS | `1` |
| `DB_ENGINE` | `sqlite` / `mysql` | `sqlite` |
| `DB_NAME` | 库名（SQLite 时为文件名） | `db.sqlite3` / `studyroom` |
| `DB_USER` / `DB_PASSWORD` | MySQL 账号密码 | `root` / 空 |
| `DB_HOST` / `DB_PORT` | MySQL 地址 | `127.0.0.1` / `3306` |
| `DB_CONN_MAX_AGE` | 连接复用秒数 | `60` |
| `DB_CHARSET` | 连接字符集 | `utf8mb4` |
| `DB_COLLATION` | 测试库排序规则 | `utf8mb4_unicode_ci` |
| `DB_SQL_MODE` | 可选，覆盖服务端 `sql_mode` | 空 |

## 数据模型

### User（用户）
继承 `AbstractUser`，新增 `role`（student/admin）、`student_id`、`phone`、`college`、`credit_score`（默认 100）。

### StudyRoom（阅览空间）
`name`、`floor`、`location`、`book_category`、`description`、`capacity`、`open_time`、`close_time`、`status`、`layout`（`{"rows":[{"count":8,"aisle_after":4}]}`，座位坐标由它推导）、`shelves`（书柜布局）。

### Seat（座位）
`room`、`seat_no`、`position_x` / `position_y`（百分比坐标）、`status`（**只有 available / unavailable**，表示管理员是否停用）。

> 座位"是否被占用"不再写入 `Seat.status`，而是由当天的 `Reservation` 推导，避免同一座位在不同日期互相覆盖状态。

### Reservation（预约）
`user`、`seat`、`date`、`start_time`、`end_time`、`status`（pending/active/completed/cancelled/noshow）、`sign_in_time`、`sign_out_time`。
带 3 个索引：`(date,status)`、`(seat,date)`、`(user,status)`。

### Book / BorrowRecord（图书 / 借阅记录）
`renew_count` 续借次数（上限 2 次）；借书/还书使用 `transaction.atomic()` + `select_for_update()`，还书与续借同时锁定借阅记录本身。

### Drink / DrinkOrder（饮品 / 订单）
`sweetness`、`temperature`、`pickup_code`（当天唯一）、`total_price`。

### Violation（违规记录）
新增自动扣信用分、删除自动回补（通过 `signals.py`，覆盖批量删除与级联删除）。

## 核心业务规则

- **签到窗口**：开始前 15 分钟 ~ 开始后 30 分钟；超时未签到由 `mark_no_shows` 记为爽约，扣 2 分
- **信用分**：`credit_score < 60` 时禁止新的预约；违规记录删除后回补
- **可用座位**：开放房间中未停用、且当天无 pending/active 预约的座位
- **借阅期限**：14 天，可续借 2 次（每次顺延 14 天）
- **并发安全**：借书/还书/续借均在事务内加行锁
- **唯一性约束**：同一用户不可同时借阅同一本书（SQLite 由条件唯一索引强约束；MySQL 不支持条件索引，由 `select_for_update()` + 应用层校验保证，详见迁移文档）
- **写操作全部走 POST**：签到/签退/取消/借还/下单/登出均带 CSRF 校验

## 生产部署注意

1. 设置 `DJANGO_SECRET_KEY` / `DJANGO_DEBUG=0` / `DJANGO_ALLOWED_HOSTS`
2. 配置反向代理与 HTTPS（`DJANGO_SECURE_SSL_REDIRECT=1`）
3. `collectstatic` 后用 Nginx/Whitenoise 托管 `staticfiles/`
4. 日志输出到 `logs/app.log`（5MB × 3 轮转）
5. 数据库推荐 MySQL 8（建库建号、数据迁移、PyCharm 配置见 `docs/PyCharm+MySQL迁移部署指南.md`）
6. 用系统计划任务定时执行 `manage.py mark_no_shows`

## 优化记录

### 第二轮：MySQL 部署支持

- `settings.py` 支持 `DB_ENGINE=sqlite|mysql` 与 `.env` 文件，MySQL 走 utf8mb4 + 连接复用 + 健康检查
- `studyroom_system/__init__.py` 增加 mysqlclient → PyMySQL 驱动兜底
- 新增 `export_data` / `import_data` 两个命令，按外键依赖顺序做 SQLite ⇄ MySQL 数据搬迁（含密码哈希、自增 ID 对齐）
- `seed_data` 现在会建 8 个房间并按容量自动生成座位（配置来自 `fixtures/rooms.json`），支持 `--with-demo-users`
- 个人中心学习时长改为跨库一致的 Python 累加（规避 MySQL 日期相减的返回类型差异）
- 依赖新增 `mysqlclient`，补充 `.env.example` 与 `docs/PyCharm+MySQL迁移部署指南.md`，测试增加到 66 个

### 第一轮：功能与性能

- 修复注册页不显示验证码导致无法注册的问题，并新增验证码刷新接口
- 签到/签退/取消预约/登出改为 POST + CSRF，消除 GET 改状态与跨站登出
- 座位状态与按日期预约解耦，`Seat.status` 只表示可用/停用（含数据迁移）
- 新增/编辑自习室自动按布局生成座位坐标，容量缩小时清理多余座位（保留有历史记录的座位）
- 新增 `services.py` / `decorators.py` / `signals.py` / `tests/`，视图拆包、路由拆分
- 管理看板 SQL 从 42 条降到 16 条，个人中心重复 COUNT 合并，后台列表补分页与真实总数
- 内联 CSS 抽到 `static/css/`（base/admin/landing 三份重复样式合并），Toast 初始化抽到 `app.js`
- settings 支持环境变量、日志与 `STATIC_ROOT`，依赖版本锁定

## 许可

开发演示项目。

