# 3d_project
为解决机房走线的混乱，在现场布线时首先用该软件计算2个端口间的走线规则
- [X] 选用几米的网线
- [X] 相同机架间走线
  - [X] 正面-正面
  - [X] 背面-背面
  - [X] 正面-背面
  - [X] 背面-正面
- [X] 不同机架间走线
  - [X] 正面-正面
  - [X] 背面-背面
  - [X] 正面-背面
  - [X] 背面-正面
- [X] 多余长度的网线如何绕圈
- [X] 2D平面展示跳纤步骤

# Requirements
[Flask](http://flask.pocoo.org/)

# Usage
1. 下载代码
> git clone git@github.com:windmin/3d_project.git
>
> cd flask-new
2. 安装依赖文件
> pip install -r requirements.txt
3. 运行
> python manager.py runserver
