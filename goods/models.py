from django.db import models

# Create your models here.
from django.db.models import Model


class Goods(Model):  # 商品信息表
    good_name = models.CharField(max_length=50,unique=True,blank=True)
    good_pic = models.ImageField(upload_to='pic/',blank=True)
    good_type = models.ForeignKey('GoodsType',on_delete=models.SET_NULL,null=True)
    good_count = models.IntegerField(blank=True)
    good_desc = models.CharField(max_length=500,blank=True)
    class Meta:
        db_table = 'tb_goods'
        verbose_name = "商品信息表"
        verbose_name_plural = verbose_name

class GoodsType(Model):
    good_type_name = models.CharField(max_length=30,unique=True,blank=False)
    class Meta:
        db_table = 'tb_goodstype'
        verbose_name = '商品类型表'
        verbose_name_plural = verbose_name



