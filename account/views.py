from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm
from django.contrib.auth import login, logout,authenticate
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import update_session_auth_hash
from PIL import Image
import datetime
from products.models import product
from django.db.models import Q
from django.core.files.base import ContentFile
from django.core.files import File
from django.contrib.auth.decorators import login_required
from . forms import user_creation_form
from index.snipt import cart_count,send_html_mail,vendor_account,added_sucessfully_msg,popups_advert
from vendor. models import vendor,vendor_bill_plan,BillPlan,free_plan_expired
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from cart.models import Order,OrderItem,billing_address,shipping_address,Top_seller



def register_view(request):
	context = {}
	context['title'] = "Register"
	cart_count(request.user,context)
	vendor_account(context,request)

	query =request.GET.get('q')
	if query:
		request.session['q'] = query
		return redirect("products:mainshop")


	if request.method =="POST":
		form = user_creation_form(request.POST)
		if form.is_valid():
			user = form.save()
			login(request,user)
			
			request.session['added_sucessfuly_msg'] = "Registration complete successfuly!!"
			return redirect('account:customer_account')
			
	else:
		form = user_creation_form()

	context['form']=form
	return render(request,"account/register.html",context)

def login_view(request):
	context = {}
	context['title'] = "LogIn"

	cart_count(request.user,context)
	vendor_account(context,request)
	
	query =request.GET.get('q')
	if query:
		request.session['q'] = query
		return redirect("products:mainshop")

	if request.method =="POST":
		username = request.POST['name']
		password = request.POST['pass']
		user = authenticate(username=username,password=password)
		if user:
			login(request,user)

			if user.is_superuser:
				return redirect('account:dashboard')
			else:
				return redirect('account:customer_account')
			
		else:
			context['error']="Provide valide Credientials!!!"
	return render(request,"account/login.html",context)

@login_required(login_url="account:google_login")
def logout_view(request):
	logout(request)
	return redirect("account:google_login")


@login_required(login_url="account:google_login")
def change_password(request):
	context = {}
	context['title'] = 'Change password'

	if request.method == 'POST':

		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
			request.session['added_sucessfuly_msg'] = "Your password was successfully updated!"
			return redirect('account:customer_account')
			
		else:
			context['error'] = "Please correct the error below."
		
	else:
		form = PasswordChangeForm(request.user)

	context['form'] = form
	return render(request, 'account/change_password.html',context)

@login_required(login_url="account:google_login")
def Dashboard(request,args=None):
	context={}
	context['title'] = "dashboard"

	cart_count(request.user,context)
	vendor_account(context,request)
	added_sucessfully_msg(request,context)

	context['search_placeholder'] ="Search oreder/ref code"

	query =request.GET.get('q')

	if request.user.is_superuser:
		cart_count(request.user,context)
		
		if args:
			order_ = Order.objects.filter(ordered=True,being_delivered=True)
		else:
			order_ = Order.objects.filter(ordered=True,being_delivered=False)

		if query:
			order_ =order_.filter(Q(ref_code=query)| 
			                      Q(ref_code=query)).distinct()

		page = request.GET.get('page', 1)
		paginator = Paginator(order_,24)

		try:
			order_ = paginator.page(page)
		except PageNotAnInteger:
			order_ = paginator.page(1)
		except EmptyPage:
			order_ = paginator.page(paginator.num_pages)

		context['orders'] = order_


		if request.is_ajax() and request.GET.get('pops'):
			pass

		elif request.is_ajax():#showing that item received from vendor by agent
			id = request.GET.get('data');
			received_item = OrderItem.objects.get(id=id)
			received_item.received_from_vendor = True
			received_item.save()

			context['order'] = Order.objects.get(id=received_item.cart.id)
			print(received_item.cart)

			html = render_to_string('cart/item_receved.html',context,request=request)
			return JsonResponse({'data':html})

		return render(request,"account/dashboard.html",context)
	else:
		return redirect('index:index')

@login_required(login_url="account:google_login")
def cart_detail(request):
	context = {}

	if request.is_ajax() and request.GET.get('pops'):#Popups/needed items ajax
		pass

	elif request.is_ajax():
		id = request.GET.get('data');
		context['order'] = Order.objects.get(id=id)

		try:
			billing_addr = billing_address.objects.filter(user=request.user).last()
			context['billing'] = billing_addr
		except billing_address.DoesNotExist:
			pass

		try:
			shipping_addr = shipping_address.objects.filter(user=request.user).last()
			context['shipping'] = shipping_addr
		except shipping_address.DoesNotExist:
			pass

		html = render_to_string('cart/cart_detail.html',context,request=request)
		return JsonResponse({'data':html})

@login_required(login_url="account:google_login")
def customer_account(request,args=None):
	context = {}
	context['title'] = "My account"

	try:#checking if user has vendor account
		profile_ = vendor.objects.get(user=request.user)
		if profile_:
			context['vendor_account'] = profile_
	except vendor.DoesNotExist:
		pass

	if request.session.has_key('added_sucessfuly_msg'):
		context['added_sucessfuly_msg'] = request.session['added_sucessfuly_msg']
		del request.session['added_sucessfuly_msg']

	cart_count(request.user,context)
	vendor_account(context,request)

	query =request.GET.get('q')

	context['search_placeholder'] ="Search oreder/ref code"

	if args:
		order_ = Order.objects.filter(user=request.user,ordered=True,being_delivered=True)
	else:
		order_ = Order.objects.filter(user=request.user,being_delivered=False)

	if query:
		order_ = order_.filter(Q(ref_code=query)| 
			                   Q(ref_code=query)).distinct()


	page = request.GET.get('page', 1)
	paginator = Paginator(order_,24)

	try:
		order_ = paginator.page(page)
	except PageNotAnInteger:
		order_ = paginator.page(1)
	except EmptyPage:
		order_ = paginator.page(paginator.num_pages)

	context['orders'] = order_

	if request.is_ajax() and request.GET.get('pops'):#Popups/needed items ajax
		popups_advert(request,context)
		html = render_to_string('index/selected_place_order.html',context,request=request)
		return JsonResponse({'data':html})

	return render(request,"account/user_account.html",context)


@login_required(login_url="account:google_login")
def bill(request):
	context = {}
	context['title'] = "Select plan"

	cart_count(request.user,context)
	vendor_account(context,request)

	context['plan'] = vendor_bill_plan.objects.all().last()

	try:
		expired_plan = free_plan_expired.objects.get(user=request.user)
		if expired_plan.expired == True:
			context['expired'] = "expired"
	except free_plan_expired.DoesNotExist:
		pass

	if request.session.has_key('bill_expired'):
		msg = request.session['bill_expired']
		context['msg_bill'] = msg
		del request.session['bill_expired']

	if request.is_ajax() and request.GET.get('pops'):#Popups/needed items ajax
		popups_advert(request,context)
		html = render_to_string('index/selected_place_order.html',context,request=request)
		return JsonResponse({'data':html})

	elif request.is_ajax():#for free payment/subscription

		current_date_time = datetime.datetime.now()#geting duedate after 30 days
		due_date_time = current_date_time + datetime.timedelta(days=30)

		try:
			free_plan = BillPlan.objects.get(user=request.user)
			free_plan.item_num =1 
			free_plan.plan = "free"
			free_plan.name = "free user"
			free_plan.actived=True#activated
			free_plan.due_date=due_date_time
			free_plan.payment_method="Mpamba"
			free_plan.ref_code="free"
			free_plan.price=0
			free_plan.save()

		except BillPlan.DoesNotExist:
			free_plan = BillPlan(user=request.user,
			                     item_num=2,
			                     plan="free",
			                     name="free user",
			                     actived=True,#activated
			                     due_date=due_date_time,
			                     payment_method="Free",
			                     ref_code="free",
			                     price=0)
			free_plan.save()

		try:
			free_plan = free_plan_expired.objects.get(user=request.user)
			pass
		except free_plan_expired.DoesNotExist:
			free_plan = free_plan_expired(user=request.user,expired=True)
			free_plan.save()


		try:#activating product-paid field after paying bill
			user_itmes = product.objects.filter(user=request.user)
			if user_itmes:
				user_itmes.update(Paid=True)

		except product.DoesNotExist:
			pass

	return render(request,"account/bill.html",context)