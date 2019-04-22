# CurriculaVariableCat_Back
超简洁选课系统(服务端)，Django REST framework。
## 展示

## 项目构建
创建虚拟环境：
```
conda env create -f env.yml
```
虚拟环境将被安装到E:/Envs/DRF下。其中XAdmin无法直接获取，使用pip安装：
```
conda activate DRF
pip install https://codeload.github.com/sshwsfc/xadmin/zip/django2
```
在本地MySQL数据库中创建该项目使用的Scheme：
```
Default collation: utf8_general_ci
Default characterset: utf8
```
然后修改CurriculaVariableCat.settings配置文件下的数据库配置。

从Model建立数据库表，使用Task指令：
```
python manage.py makemigrations
python manage.py migrate
```
提取XAdmin所使用静态文件，使用Task指令：
```
python manage.py collectstatic
```
创建超级用户，使用Task指令：
```
python manage.py createsuperuser
```
> 若使用PyCharm，可以在Tools->run manage.py Task调出Task指令的Terminal，使用时无需再输入`python manage.py`。

## 项目运行
```
python manage.py runserver localhost:8000
```
若在PyCharm中运行，添加Environment Variables：
```
DJANGO_SETTINGS_MODULE=CurriculaVariableCat.settings
PYTHONUNBUFFERED=1
```
## 前端项目地址
[CurriculaVariableCat_Front](https://github.com/LauZyHou/CurriculaVariableCat_Front)