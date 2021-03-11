from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View
from django import http
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
import re

from goods.models import Goods,GoodsType
from django.db import DatabaseError
from django.db.models import Count

class TjView(View):
    def get(self,request):
        good_type_name = []
        good_type_count = []
        # goods = Goods.objects.annotate(c=Count('good_type')).values('good_type','c')
        counts = Goods.objects.values('good_type').annotate(c=Count('good_type'))
        count_list =[]
        for count in counts:
            name = GoodsType.objects.get(id=count['good_type']).good_type_name

            total = Goods.objects.filter(good_type_id=count['good_type'])
            goodscount = 0
            for item in total:
                goodscount += item.good_count
            count_list.append(goodscount)
            good_type_name.append(name)
            good_type_count.append(count['c'])
        content = {
            'count_list':count_list,
            'good_type_name':good_type_name,
            'good_type_count':good_type_count,
        }

        # print(content)
        # for good in goods:
        #     good.good_type.good_type_name
        # print(c)
        # goodstype = GoodsType.objects.order_by('id')
        # goods = Goods.objects.get(id=1)
        # type = goods.good_type.good_type_name
        # type = GoodsType.objects.get(good_type_name='浴室柜')
        # goods = type.goods_set.all()
        # for good in goods:
        #     print(good.good_name)

        # for type in goodstype:
        #     leixing = type.goodstype.good_type_name
        #     # good_type_name.append(type.good_type_id)
        # print(goods)
        return render(request,'tj.html',content)

class GoodstypelistView(LoginRequiredMixin,View):
    def get(self,request):
        goodstype = GoodsType.objects.order_by('id')
        content={
            'goodstype':goodstype,
        }
        return render(request,'goodstype.html',content)
    def post(self,request):
        typeid = request.POST.get('typeid')
        typename = request.POST.get('typename')
        goodstype = GoodsType.objects.get(id=typeid)
        goodstype.good_type_name = typename
        goodstype.save()
        return redirect(reverse('goods:goodstype'))
class DeletetypeView(LoginRequiredMixin,View):
    def get(self,request,typeid):
        GoodsType.objects.get(id=typeid).delete()
        return redirect(reverse('goods:goodstype'))


class AddGoodstypeView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'addgoodstype.html')
    def post(self,request):
        goodstype = request.POST.get('goodstype')
        if goodstype is None:
            return http.HttpResponseForbidden('请输入类型')
        if GoodsType.objects.filter(good_type_name=goodstype):
            return http.HttpResponse('类型已经存在')
        GoodsType.objects.create(good_type_name=goodstype)
        return redirect(reverse('goods:addgoods'))
        # return http.HttpResponse('添加成功')


class GoodsListView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'index.html')
class AddGoodsView(LoginRequiredMixin,View):
    def get(self,request):
        goodstype = GoodsType.objects.all()
        context = {
            'goodstype':goodstype,
        }

        return render(request,'addgoods.html',context=context)

    def post(self,request):

        goodsname = request.POST.get('goodsname')
        goodstype = request.POST.get('goodstype')
        goodscount = int(request.POST.get('goodscount'))
        goodsdesc = request.POST.get('goodsdesc')
        if not all([goodsname,goodstype,goodscount]):
            return http.HttpResponseForbidden('参数不全')

        if not isinstance(goodscount,int):
            return http.HttpResponseForbidden('数量必须为数字')
        # 如果首次添加则创建，否则只累加数量
        # print(Goods.objects.filter(good_name=goodsname))
        if not Goods.objects.filter(good_name=goodsname):
            goodtypes = GoodsType.objects.filter(good_type_name=goodstype).first()
            Goods.objects.create(good_name=goodsname,good_count=goodscount,good_type=goodtypes,good_desc=goodsdesc)
        else:
            goods = Goods.objects.get(good_name=goodsname)
            goods.good_count = goods.good_count + goodscount
            goods.save()
        return redirect('user:index')

        # return http.HttpResponse('添加成功')
class GoodsinfoView(LoginRequiredMixin,View):
    def get(self,request,goodsid):
        goodsinfo = Goods.objects.filter(id=goodsid).first()
        # type = goodsinfo.good_type.good_type_name
        goodstype = GoodsType.objects.all()
        content = {
            'goodsinfo': goodsinfo,
            'goodstype':goodstype,
        }
        return render(request,'goodsinfo.html',content)
    def post(self,request,goodsid):
        goodsname = request.POST.get('goodsname')
        goodspic = request.FILES.get('goodspic')
        goodstype = request.POST.get('goodstype')
        goodscount = request.POST.get('goodscount')
        goodsdesc = request.POST.get('goodsdesc')
        if not all([goodsname,goodstype,goodscount,goodsdesc]):
            return http.HttpResponseForbidden('参数不全')
        goods = Goods.objects.get(id=goodsid)
        goods.good_name = goodsname
        goods.good_pic = goodspic
        goods.good_type_id = goodstype
        goods.good_count = goodscount
        goods.good_desc = goodsdesc
        goods.save()
        # return render(request,'index.html')
        # return http.HttpResponse('添加成功')
        return redirect(reverse('user:index'))
class DeletegoodsView(View):
    def get(self,request,goodsid):
        Goods.objects.get(id=goodsid).delete()
        return redirect(reverse('user:index'))
class GoodstypeView(LoginRequiredMixin,View):
    def get(self,request):
        goodstype = GoodsType.objects.all()
        content = {
            'goodstype':goodstype,
        }
        return render(request,'goodstype.html',content)

