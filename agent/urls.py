from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = 'agentmanage'
urlpatterns = [
	url(r'^admin/agent/agent/$', views.agent, name='agent'),
	url(r'^admin/agent/agent/add/$', views.agent_add, name='agent_add'),
	url(r'^admin/agent/agent/(\d+)/change/$', views.agent_change, name='agent_change'),
	url(r'^admin/agent/carmel/add/$', views.carmel_add, name='carmel_add'),
	url(r'^admin/agent/carmel/(\d+)/change/$', views.carmel_change, name='carmel_change'),
	url(r'^admin/agent/user$', views.user, name='user'),
	url(r'^admin/', admin.site.urls),
]