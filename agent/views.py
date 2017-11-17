from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from agent.models import *
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User, Group

def agent(request):
	if request.method == "GET":
		superior = Agent.objects.get(username=request.user.username)
		agents = Agent.objects.filter(superior = superior)
		manage_name = request.user.username
		data = {'agents': agents, 'count': len(agents), 'manage_name': manage_name}
		return render(request, 'agent.html', data)
	else:
		if request.POST['action'] == "delete_selected":
			choice_id = int(request.POST['_selected_action'])
			agent = Agent.objects.get(id=choice_id)
			User.objects.get(username=agent.username).delete()
			agent.delete()
			return HttpResponseRedirect(reverse("agent"))

def agent_add(request):
	if request.method == "GET":
		superior = Agent.objects.get(username = request.user.username)
		manage_name = request.user.username
		invite_code = get_invite()
		data = {'superior': superior, 'manage_name': manage_name, "invite_code": invite_code}
		return render(request, 'agent_add.html', data)
	else:
		superior = Agent.objects.get(username=request.user.username)
		consume_point = int(request.POST['consume_point'])

		if ( len(Agent.objects.filter(username = request.POST['username'])) > 0 ):
			return render(request, 'agent_add.html', {'error': '此用户已存在'})

		if ( consume_point > superior.consume_point):
			return render(request, 'agent_add.html', {'error': '最多可设置%s点'%superior.consume_point})


		agent = Agent.objects.create(username = request.POST['username'],
			password = make_password(request.POST['password']),
			mobile = request.POST['mobile'],
			wechat = request.POST['wechat'],
			e_mail = request.POST['e_mail'],
			agent_class = superior.agent_class + 1,
			invite_code = get_invite(),
			superior = superior,
			consume_point = consume_point,
			)
		# auth_user regis
		user = User.objects.create(username = agent.username,
								   password = make_password(request.POST['password']),
								   is_superuser = 0,
								   is_staff = 1,
								   is_active = 1,
								   )
		group = Group.objects.get(name="代理")
		user.groups.add(group)
		user.save()
		# sub consume_point
		superior.consume_point -=  consume_point
		superior.save()
		return HttpResponseRedirect(reverse("agent"))

def agent_change(request, agent_id):
	if request.method == "GET":
		agent = Agent.objects.get(id=agent_id)
		manage_name = request.user.username
		data = {'agent': agent, 'manage_name': manage_name}
		return render(request, 'agent_change.html', data)
	else:
		superior = Agent.objects.get(username=request.user.username)
		consume_point = int(request.POST['consume_point'])

		# if ( len(Agent.objects.filter(username = request.POST['username'])) > 0 ):
		# 	return render(request, 'agent_change.html', {'error': '此用户已存在'})

		if ( consume_point > superior.consume_point):
			return render(request, 'agent_change.html', {'error': '最多可设置%s点'%superior.consume_point})

		agent = Agent.objects.get(id = int(request.POST['id']))
		agent.password = make_password(request.POST['password'])

		user = User.objects.get(username = agent.username)
		user.password = make_password(request.POST['password'])
		user.save()

		agent.mobile = request.POST['mobile']
		agent.wechat = request.POST['wechat']
		agent.e_mail = request.POST['e_mail']
		agent.consume_point = consume_point	
		agent.save()
		return HttpResponseRedirect(reverse('agent'))



def carmel_add(request):
	if request.method == "GET":
		agent = Agent.objects.get(username = request.user.username)
		carmel_code = get_carmel()
		data = {'agent': agent, 'carmel_code': carmel_code}
		return render(request, 'carmel_add.html', data)
	else:
		d = {"月卡": 1, "季卡": 2, "年卡": 4, "空卡": 0}
		Carmel.objects.create(code = request.POST['code'],
			type_class = request.POST['type_class'],
			point = d[request.POST['point']],
		)
		agent = Agent.objects.get(username = request.user.username)
		agent.consume_point -= d[request.POST['type_class']]
		agent.save()
		return render(request, '/carmel/carmel')

def carmel_change(request, carmel_id):
	if request.method == "GET":
		agent = Agent.objects.get(username = request.user.username)
		carmel = Carmel.objects.get(id = carmel_id)
		data = {'agent': agent, 'carmel': carmel}
		return render(request, "carmel_change.html", data)
	else:
		agent = Agent.objects.get(username = request.user.username)
		carmel = Carmel.objects.get(id=request.POST['id'])
		d = {"月卡": 1, "季卡": 2, "年卡": 4, "空卡": 0}
		agent.consume_point -= d[request.POST['type_class']] - carmel.point
		agent.save()

		carmel.point = d[request.POST['type_class']]
		carmel.type_class = request.POST['type_class']
		carmel.save()

		return HttpResponseRedirect("/admin/agent/carmel/")

def user(request):
	agent = Agent.objects.get(username = request.user.username)
	return HttpResponseRedirect("/admin/agent/user/?superior__id__exact=%d" % agent.id)




def get_invite():
	from string import ascii_uppercase
	invite = ''
	while(True):
		invite = ''
		chars = ascii_uppercase + "0123456789"
		for i in range(6):
			invite += choice(chars)
		if ( len(Agent.objects.filter(invite_code=invite)) == 0):
			break;
	return invite

def get_carmel():
	import hashlib
	import time
	return hashlib.md5(str(time.time()).encode('utf-8')).hexdigest()