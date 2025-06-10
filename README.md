# life description
Website for picture uploading and display



### 1. 网站功能

##### 用户系统
- 注册/登录/注销
- 个人资料页面

##### 图片功能
- 上传图片（支持JPG/PNG格式）
- 自动生成缩略图
- 分页浏览图片
- 图片详情查看

##### 评论系统
- 发表评论
- 回复评论
- 嵌套评论显示

##### 其他功能
- 深色/浅色模式切换
- 响应式设计（适配手机/平板/桌面）
- 本地图片存储
- SQLite数据库



### 2. 管理网站

- 停止网站：在终端按 Ctrl+C
- 重新启动：再次运行 python run.py
- 查看数据库：使用 sqlite3 lifeshare.db
- 备份图片：备份 uploads 目录



# Install Dependency

pip install flask flask-sqlalchemy flask-login flask-wtf pillow



# User Guide

### Initial SQLite
first run `python run.py`, it will create the local database

### Run Service
run `python run.py` again

