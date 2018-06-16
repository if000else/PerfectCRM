from django.db import models

# Create your models here.

class TestModel(models.Model):
    name = models.CharField(verbose_name='姓名',max_length=16,null=True,blank=True)
    mobile = models.PositiveIntegerField(verbose_name='手机号')