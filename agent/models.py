from django.db import models
from django.utils import timezone
from random import choice

class Agent(models.Model):
	class_choice = (
		(1, '1'),
		(2, '2'),
		(3, '3'),
		(4, '4'),
		(5, '5'),
	)

	# 生成邀请码
	def get_invite():
		from string import ascii_uppercase
		chars = ascii_uppercase + "0123456789"
		invite = ''
		for i in range(6):
			invite += choice(chars)
		return invite

	username = models.CharField(u'账号', max_length=100, unique=True)
	mobile = models.CharField(u'手机', max_length=11, blank=True, default='')
	wechat = models.CharField(u'微信', max_length=50, blank=True)
	e_mail = models.EmailField(u'邮箱', blank=True)
	password = models.CharField(u'密码', max_length=50)
	agent_class = models.SmallIntegerField(u'VIP等级', choices=class_choice)
	consume_point = models.IntegerField(u'点数', default=0)
	invite_code = models.CharField(u'邀请码', max_length=6, default=get_invite, editable=True)
	superior = models.ForeignKey("Agent", on_delete=models.SET_NULL, verbose_name='上级代理', blank=True, null=True)
	create_time = models.DateTimeField(u'创建时间', auto_now_add=True)

	def __str__(self):
		return self.username

	class Meta:
		verbose_name = '代理'
		verbose_name_plural = '代理'
		ordering = ['agent_class']


class Carmel(models.Model):
	carmel_type = (
		("空卡", "空卡 -- 0"),
		("月卡", "月卡 -- 1"),
		("季卡", "季卡 -- 2"),
		("年卡", "年卡 -- 4"),
	)
	status_choice = (
		(0, '未使用'),
		(1, '已使用'),
	)

	def get_carmel():
		import hashlib
		import time
		return hashlib.md5(str(time.time()).encode('utf-8')).hexdigest()

	code = models.CharField(u'卡密', max_length=32, default=get_carmel)
	type_class = models.CharField(u'类型', choices=carmel_type, max_length=20)
	point = models.SmallIntegerField(u'点数', default=get_carmel, editable=False)
	status = models.SmallIntegerField(u'状态', default=0, editable=False, choices=status_choice)
	create_time = models.DateTimeField(u'创建时间', auto_now_add=True)

	def __str__(self):
		return self.code

	class Meta:
		verbose_name = "卡密"
		verbose_name_plural = "卡密"
		ordering = ['-create_time']


class User(models.Model):
	class_choice = (
		('注册会员', '注册会员'),
		('月度会员', '月度会员'),
		('季度会员', '季度会员'),
		('年度会员', '年度会员'),
	)
	mobile = models.CharField(u'手机', max_length=20)
	password = models.CharField(u'密码', max_length=50)
	superior = models.ForeignKey("Agent", on_delete=models.SET_NULL, verbose_name='推荐人', blank=True, null=True)
	vip_class = models.CharField(u'会员等级', choices=class_choice, default='注册会员', max_length=20)
	vip_date = models.DateTimeField(u'VIP到期时间', auto_now_add=True)
	create_time = models.DateTimeField(u'创建时间', auto_now_add=True)

	def __str__(self):
		return self.mobile

	class Meta:
		verbose_name = "会员"
		verbose_name_plural = "会员"
		ordering = ['-create_time']