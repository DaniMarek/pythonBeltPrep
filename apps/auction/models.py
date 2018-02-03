from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REGEX=re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

class UserManager(models.Manager):
	def reggie_validation(self, POSTdata):
		errors = []
		if len(POSTdata['first_name']) < 2:
			errors.append('first name must be more than 2 characters')
		if len(POSTdata['last_name']) < 2:
			errors.append('last name must be more than 2 characters')
		if len(POSTdata['password']) < 2:
			errors.append('password must be more than 2 characters')
		if POSTdata['password'] != POSTdata['password_confirmation']:
			errors.append('passwords must match!')
		if re.match(EMAIL_REGEX, POSTdata['email']):
			if len(POSTdata['email']) < 11:
				errors.append('not a valid email address!')
		if not re.match(EMAIL_REGEX, POSTdata['email']):
			errors.append('not a valid email address!')
		return errors

	def login_validation(self, POSTdata):
		errors = []
		user = User.objects.filter(email=POSTdata['email']).first()

		if re.match(EMAIL_REGEX, POSTdata['email']):
			if len(POSTdata['email']) < 11:
				errors.append('not a valid email address!')
		if not re.match(EMAIL_REGEX, POSTdata['email']):
			errors.append('not a valid email address!')
		if len(POSTdata['password']) < 2:
			errors.append('incorrect password')
		if user:
			user_password = POSTdata['password'].encode()
			db_password = user.password.encode()
			if bcrypt.checkpw(user_password, db_password):
				return {'user':user}
		return {'errors':errors}

		return errors
		
	def create_user(self, POSTdata):
		hashedpw = bcrypt.hashpw(POSTdata['password'].encode(), bcrypt.gensalt())
		return User.objects.create(
			first_name = POSTdata['first_name'],
			last_name = POSTdata['last_name'],
			email = POSTdata['email'],
			password = hashedpw,
			)

class ItemManager(models.Manager):
	def item_validation(self, POSTdata):
		errors = []
		if len(POSTdata['item']) < 2:
			errors.append('item name must be more than 2 characters')
		if len(POSTdata['description']) < 2:
			errors.append('description must be more than 2 characters')
		if POSTdata['price'] < 1:
			errors.append('starting bid must be at least $1.00')
		return errors

	def create_item(self, POSTdata):
		return Item.objects.create(
	  		item = POSTdata['item'],
			description = POSTdata['description'],
			price = POSTdata['price'],
			end_date = POSTdata['end_date'],
	  		)


class User(models.Model):
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  email = models.CharField(max_length=255)
  wallet = models.IntegerField(default=1000)
  password = models.CharField(max_length=255)

  objects=UserManager()

  def __unicode__(self):
  	return  'first_name:{}, last_name:{}, email:{}, wallet:{}, password:{}, id:{}'.format(self.first_name, self.last_name, self.email, self.wallet, self.password, self.id)

class Item(models.Model):
  item = models.CharField(max_length=255)
  price = models.IntegerField()
  description = models.TextField(max_length=255)
  # time_remaining = models.CharField(max_length=255, null=False)
  end_date = models.DateField()
  user = models.ForeignKey(User, related_name="items")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  bidder = models.ForeignKey(User, null=True, related_name="bidder")
  objects=ItemManager()

  def __unicode__(self):
  	return  'item:{}, description:{}, price:{}, end_date:{}, id:{}, user:{}, bidder:{}'.format(self.item, self.description, self.price, self.end_date, self.id, self.user, self.bidder)