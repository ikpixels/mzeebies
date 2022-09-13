from django.db import models
from django.contrib.auth.models import User

def upload_profile(instance,filename):
	basename,extension =filename.split('.')
	return "%s/%s.%s"%( 'domain_name_here',instance.fullName,extension)

class vendor(models.Model):
	user = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
	fullName = models.CharField(max_length=100)
	phoneWapNum  = models.PositiveIntegerField()
	Adress       = models.CharField(max_length=100)
	district     = models.CharField(max_length=100)
	area         = models.CharField(max_length=100)
	mobile_payment_name  = models.CharField(max_length=100,blank=True,null=True)
	mobile_payment_no  = models.PositiveIntegerField(default=0)
	bankAccType  = models.CharField(max_length=100)
	bankAccName  = models.CharField(max_length=100)
	bankAccType  = models.CharField(max_length=100)
	bankAccBrach = models.CharField(max_length=100)
	bankAccNumm  = models.PositiveIntegerField()
	password     = models.CharField(max_length=200,blank=True,null=True)#not used or delete this field
	secretKey    = models.CharField(max_length=100,blank=True,null=True)
	file         = models.ImageField(upload_to=upload_profile,blank=True,)

	def __str__(self):
		return self.fullName



class BillPlan(models.Model):

	METHOD = (('airtel','Airel Money'),('TNM','Mpamba'))
	user  = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
	plan  = models.CharField(max_length = 100)
	name  = models.CharField(max_length = 100)
	payment_method = models.CharField(max_length = 100,choices=METHOD)
	payment_date   = models.DateTimeField(auto_now=True)
	ref_code = models.CharField(max_length = 100)
	price = models.DecimalField(max_digits=18, decimal_places=2,default=0)
	item_num = models.PositiveIntegerField(default =0)#required num of items depending on selected plan
	item_num2 = models.PositiveIntegerField(default =0)#entered items before due date(if this field num == item_num, user will not allowed to add any items if )
	actived  = models.BooleanField(default=False)
	due_date = models.DateTimeField(auto_now_add=False, blank=True, null=True)

	def __str__(self):
		return self.name


class vendor_bill_plan(models.Model):
	rate   =  models.PositiveIntegerField(default=0)
	airtel_money_for_item  =  models.PositiveIntegerField(default=0)
	mpamba_money_for_item  =  models.PositiveIntegerField(default=0)
	airtel_money_for_bill  =  models.PositiveIntegerField(default=0)
	mpamba_money_for_bill  =  models.PositiveIntegerField(default=0)
	airtel_money_for_deal  =  models.PositiveIntegerField(default=0)
	mpamba_money_for_deal  =  models.PositiveIntegerField(default=0)
	deal_price  = models.DecimalField(max_digits=18, decimal_places=2,default=0)
	price  = models.DecimalField(max_digits=18, decimal_places=2,default=0)
	silver = models.DecimalField(max_digits=18, decimal_places=2,default=0)
	gold   = models.DecimalField(max_digits=18, decimal_places=2,default=0)
	platinum = models.DecimalField(max_digits=18, decimal_places=2,default=0)
	info     = models.TextField(blank=True,null=True)
	
	def __str__(self):
		return "payment plan"


class free_plan_expired(models.Model):
	user  = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
	expired  = models.BooleanField(default=False)

	def __str__(self):
		return "expired"


def agent_profile(instance,filename):
	basename,extension =filename.split('.')
	return "%s/%s.%s"%( 'domain_name_here',instance.last_name,extension)

class agent_info(models.Model):#branch model
    user        =  models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
    title       =  models.CharField(max_length=100)
    first_name  =  models.CharField(max_length=100)
    last_name   =  models.CharField(max_length=100)
    phonenumber =  models.PositiveIntegerField()
    email       =  models.EmailField()
    district    =  models.CharField(max_length=100)
    area        =  models.CharField(max_length=100)
    adress      =  models.CharField(max_length=100,blank=True,null=True)
    agent       = models.BooleanField(default=True)
    file        =  models.ImageField(upload_to=agent_profile,blank=True)

    def __str__ (self):
    	return self.first_name + " " + self.last_name

    def phone_number(self):
    	code = (str(self.phonenumber)[:3])
    	digits = (str(self.phonenumber)[3:])
    	phone_number = "+" + "(" + code + ")" + " " + digits
    	return phone_number

class deal_payment(models.Model):

	METHOD = (('airtel','Airel Money'),('TNM','Mpamba'))
	user   = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
	period = models.PositiveIntegerField(default =0)
	name   = models.CharField(max_length = 100)
	payment_method = models.CharField(max_length = 100,choices=METHOD)
	payment_date   = models.DateTimeField(auto_now=True)
	ref_code  = models.CharField(max_length = 100)
	new_item_price = models.PositiveIntegerField(default =0) 
	item_id   = models.PositiveIntegerField(default =0) 
	amount    = models.DecimalField(max_digits=18, decimal_places=2,default=0)
	Verified  = models.BooleanField(default=False)

	def __str__(self):
		return self.name