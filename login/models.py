from django.db import models

# Create your models here.


class sora_UserInfo(models.Model):
    account = models.CharField(verbose_name="账户名称",max_length=32)
    password = models.CharField(verbose_name="密码",max_length=128)
    email = models.CharField(verbose_name="邮箱",max_length=32)
    name = models.CharField(verbose_name="姓名",max_length=32)
    phone = models.IntegerField(verbose_name="手机号码")
    salt = models.CharField(verbose_name="salt",max_length=128)
