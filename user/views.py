from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views import View
# from django_redis import get_redis_connection
from django import http
from django.db import DatabaseError
import re
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from user.models import User
from goods.models import Goods
from user.captcha.captcha import captcha


# class ImageCodeView(View):
#     def get(self,request,uuid):
#         text,image = captcha.generate_captcha()
#         redis_con = get_redis_connection('verify_code')
#         redis_con.setex('img_%s'%uuid,300,text)
#         return http.HttpResponse(image,content_type='image/jpg')
class TestView(View):
    def get(self,request):
        return render(request,'test.html')
class LogoutView(View):
    def get(self,request):
        logout(request)
        # request.delete_cookie()
        return render(request,'login.html')

class LoginView(View):
    def get(self,request):
        return render(request,'login.html')
    def post(self,request):
        # 接收参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        # 校验参数
        if not all([username,password,password2]):
            return http.HttpResponseForbidden('参数不全')
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$',username):
            return http.HttpResponseForbidden('用户名不符合要求')
        if not re.match(r'^[a-zA-Z0-9]{8,20}$',password):
            return http.HttpResponseForbidden('密码不符合要求')
        if password2 != password:
            return http.HttpResponseForbidden('两次密码不一致')
        # 验证登陆
        user = authenticate(username=username,password=password)
        if user is None:
            return render(request,'login.html',{'account_errmsg':'用户名或密码错误'})
        login(request,user)
        request.session.set_expiry(0)
        # 登陆成功，跳转到首页
        next = request.GET.get('next')
        if next:
            response = redirect(next)
        else:
            response = redirect(reverse('user:index'))

        return response


class IndexView(LoginRequiredMixin,View):
    def get(self,request):
        # sort = request.GET.get('sort','id')
        goods_list = []
        page_num = request.GET.get('page_num',1)
        goods = Goods.objects.order_by('id')
        for good in goods:
            goods_list.append(good.good_name)
        count = goods.count()
        paginator = Paginator(goods,10)
        page_goods = paginator.page(page_num)
        # total_page = paginator.num_pages
        context = {
            'goods_list':goods_list,
            'count':count,
            'page_goods':page_goods,
            'page_num':page_num,
        }
        return render(request,'index.html',context)


class RegisterView(View):
    def get(self,request):
        return render(request,'register.html')
    def post(self,request):
        # 接收参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        # 校验参数
        if not all([username,password,password2]):
            return http.HttpResponseForbidden('缺少必要参数')
        if not re.match(r'[a-zA-Z0-9_-]{5,20}',username):
            return http.HttpResponseForbidden('用户名格式错误')
        if not re.match(r'[a-zA-Z0-9]{8,20}',password):
            return http.HttpResponseForbidden('密码格式错误')
        if password != password2:
            return http.HttpResponseForbidden('两次密码不一致')
        try:
            user = User.objects.create_user(username=username,password=password)
        except DatabaseError:
            return render(request,'register.html',{"register_errmsg":"注册失败"})
        login(request,user)   # 注册成功，自动登陆，跳转到首页
        request.session.set_expiry(0)  #设置会话时间，浏览器关闭即失效
        return render(request,'index.html')