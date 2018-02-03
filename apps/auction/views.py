from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from .models import User, Item
from django.contrib import messages
from datetime import datetime

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
	item = Item.objects.all()

	context={
		'user': current_user(request),
		'item': item,
		'time': datetime.now().date()
	}
	request.session['msg'] = 'Welcome Back, '

	for i in item:
		time_remaining = i.end_date - datetime.now().date()
		# i.save()
		print time_remaining
		if time_remaining == 0:
			i.user.wallet = i.user.wallet + i.price
			i.bidder.wallet = i.bidder.wallet - i.price

	return render(request, 'auction/main.html', context)

def successreg(request):
	item = Item.objects.all()

	context={
		'user': current_user(request),
		'item': item,
	}
	request.session['msg'] = 'Thanks for signing up, '
	return render(request, 'auction/main.html', context)

def logout(request):
	if 'user_id' in request.session:
		request.session.pop('user_id')
	return redirect('/')

def additem(request):
	user = current_user(request)
	if request.method == 'POST':
		errors = Item.objects.item_validation(request.POST)
		if not errors:	
			item = Item.objects.create(item = request.POST['item'], user=user,
		description = request.POST['description'],
		price = request.POST['price'],
		end_date = request.POST['end_date'])	
			
			return redirect('/successlog')
		flash_errors(errors, request)
	return redirect('/new')

def new(request):
	return render(request, 'auction/new.html')

def delete(request, id):
	user = User.objects.get(id=request.session['user_id'])
	item = Item.objects.get(id=id)
	if item.user == user:
		item.delete()
	return redirect('/successlog')

def list_items(request):
	return Item.objects.get(id=request.session['item_id'])

def bid(request, id):
	# user = User.objects.get(id=request.session['user_id'])
	item = Item.objects.get(id=id)	
	user = User.objects.get(id=item.user.id)
	context={
		'user': user,
		'item': item,
		'time': datetime.now().date()
	}	
		# errors = User.objects.reggie_validation(request.POST)
		# if not errors:
			# return redirect('/successreg')
	# flash_errors(errors, request)
	return render(request, 'auction/bid.html', context)

def newbid(request, id):
	user = User.objects.get(id=request.session['user_id'])
	# bidder = User.objects.get(id=request.session['user_id'])
	item = Item.objects.get(id=id)
	bid = request.POST['bid_item']
	print user.wallet
	if user.wallet > bid and bid > item.price:
		item.bidder = user
		# item.save()

		# item1=Item.objects.get(id=id)
		item.price=bid
		item.price.save(force_update=True)


	return redirect('/bid/' + id)

def home(request):
  return render(request, 'auction/main.html')