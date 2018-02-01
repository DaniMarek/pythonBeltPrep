from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from .models import User
from django.contrib import messages

def index(request):
  return render(request, 'auction/index.html')

def flash_errors(errors, request):
	for error in errors:
		messages.error(request, error)

def user_session(request):
	return User.objects.get(id = request.session['user_id'])

def registration(request):
	if request.method == 'POST':
		errors = User.objects.reggie_validation(request.POST)
		if not errors:
			user = User.objects.create_user(request.POST)
			request.session['user_id'] = user.id
			return redirect('/successreg')
		flash_errors(errors, request)
	return redirect('/')

def login(request):
	if request.method == 'POST':
		check = User.objects.login_validation(request.POST)
		if 'user' in check:
			print check
			request.session['user_id']=check['user'].id
			return redirect('/successlog')
		flash_errors(check['errors'],request)
	return redirect('/')

def current_user(request):
	return User.objects.get(id=request.session['user_id'])

def successlog(request):
	context={
		'user': current_user(request),
	}
	request.session['msg'] = 'Welcome Back, '
	return render(request, 'auction/main.html', context)

def successreg(request):
	context={
		'user': current_user(request),
	}
	request.session['msg'] = 'Thanks for signing up, '
	return render(request, 'auction/main.html', context)

def logout(request):
	if 'user_id' in request.session:
		request.session.pop('user_id')
	return redirect('/')
