from django.contrib import admin
from .models import Agent, Carmel, User
from django.contrib.admin.views.main import ChangeList

class AgentAdmin(admin.ModelAdmin):
	# list_display = ('username', 'agent_class', 'consume_point', 'invite_code', 'superior')
	list_display = ('username', 'mobile', 'consume_point', 'invite_code', 'create_time')
	list_filter = ['superior', 'agent_class']
	readonly_fields = ['invite_code']
	search_fields = ('username', 'agent_class')
	raw_id_fields = ("superior",)
	list_per_page = 20

	def save_model(self, request, obj, form, change):
		super(AgentAdmin,self).save_model(request, obj, form, change)

		from django.contrib.auth.models import User, Group
		from django.contrib.auth.hashers import make_password, check_password
		user = User.objects.create(username = obj.username,
								   password = make_password(obj.password),
								   is_superuser = 0,
								   is_staff = 1,
								   is_active = 1,
								   )
		group = Group.objects.get(name="代理")
		user.groups.add(group)
		user.save()

	def delete_model(self, request, obj):
		super(AgentAdmin, self).delete_model(request, obj)
		from django.contrib.auth.models import User, Group
		from django.contrib.auth.hashers import make_password, check_password
		User.objects.get(username=obj.username).delete()

	# def change_view(self, request, object_id, extra_context=None):
	# 	if request.method == "GET":
			
	# 	if request.method == "POST":
	# 		request.POST = request.POST.copy()
	# 		request.POST['text'] += '12321'
	# 	return super(AnnouncementAdmin,self).change_view(request, object_id, extra_context)


class CarmelAdmin(admin.ModelAdmin):
	list_display = ('code', 'type_class', 'status')
	list_filter = ['type_class', 'status' ]
	readonly_fields = ['code']
	search_fields = ('text',)

class UserAdmin(admin.ModelAdmin):
	list_display = ('id', 'mobile', 'create_time', 'vip_date', 'vip_class')
	list_filter = ['superior', 'vip_class']
	readonly_fields = ['superior', 'vip_class', 'mobile']

	# def changelist_view(self, request, extra_context=None):
	# 	if request.user.has_perm("main.delete_announcement"):
	# 		cl = ChangeList(request, search_fields=('username'))
	# 	filtered_query_set = cl.get_query_set(request)
	# 	extra_context['filtered_query_set'] = filtered_query_set
	# 	return super(UserAdmin, self).changelist_view(request, extra_context)


admin.site.register(Carmel, CarmelAdmin)
admin.site.register(Agent, AgentAdmin)
admin.site.register(User, UserAdmin)
