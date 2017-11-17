"""admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = 'admin123'
urlpatterns = [
	url(r'^admin/agent/agent/$', views.agent, name='agent'),
	url(r'^admin/agent/agent/add/$', views.agent_add, name='agent_add'),
	url(r'^admin/agent/agent/(\d+)/change/$', views.agent_change, name='agent_change'),
	url(r'^admin/agent/carmel/add/$', views.carmel_add, name='carmel_add'),
	url(r'^admin/agent/carmel/(\d+)/change/$', views.carmel_change, name='carmel_change'),
	url(r'^admin/agent/user$', views.user, name='user'),
	url(r'^admin/', admin.site.urls),
]