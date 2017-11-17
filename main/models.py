from django.db import models
from django.utils import timezone

class Announcement(models.Model):
	text = models.TextField(u'公告内容')
	create_time = models.DateTimeField(u'创建时间', auto_now_add=True)

	def __str__(self):
		return self.text[:15]

	class Meta:
		verbose_name = '公告'
		verbose_name_plural = '公告'
		ordering = ['-create_time']

class Version(models.Model):
	version = models.CharField(u'版本号', max_length=20)
	mark = models.TextField(u'版本更新提示', blank=True)
	update_url = models.URLField(u'更新地址')

	def __str__(self):
		return self.version

	class Meta:
		verbose_name = '版本'
		verbose_name_plural = '版本'
		ordering = ['version']

class Live(models.Model):
	show_image = models.ImageField(r'展示图片', upload_to="live")
	name = models.CharField(u'机构名', max_length=100)
	anchor_count = models.IntegerField(u'主播数', blank=True)
	url = models.CharField(u'播放链接', max_length=1000)
	create_time = models.DateTimeField(u'添加时间', auto_now_add=True)
	summary = models.TextField(u'平台简介')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = '直播平台'
		verbose_name_plural = '直播平台'
		ordering = ['name']