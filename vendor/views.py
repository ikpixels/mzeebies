from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from products.models import product,Popular,Categories,category_banner,Brand
from . forms import VendorForm,billform,bill_verification_form,AgentForm
from . models import vendor,vendor_bill_plan,BillPlan,free_plan_expired,agent_info,deal_payment
from index.snipt import cart_count,send_html_mail,vendor_account,secret_code,popups_advert
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.template.loader import render_to_string
from cart.models import OrderItem
from products.models import product
import datetime
 

@login_required(login_url="account:google_login")
def Vendor(request,):#Vendor form
	context = {}

	context['title'] = "Become our Vendor"
	cart_count(request.user,context)

	#vendor_account(context,request)

	try: #UNIQUE constraint
		profile = vendor.objects.get(user=request.user)
		if profile:
			request.session['vendor_error'] = "You have already created vendor account!!"
			return redirect('vendor:vendor_account')

	except vendor.DoesNotExist:
		if request.method =="POST":
			form = VendorForm(request.POST,request.FILES)
			if form.is_valid():
				instance = form.save()
				instance.user = request.user
				instance.secretKey = secret_code()
				instance.save()
				return redirect('account:bill')
		else:
			form = VendorForm()
	context['form'] = form
	return render(request,'index/form.html',context)

@login_required(login_url="account:google_login")
def EditVendor(request,id=None):
	context = {}

	context['title'] = "Edit vendor account"
	cart_count(request.user,context)
	#vendor_account(context,request)
	
	if id:
		Vendor = vendor.objects.get(id=id)

	if request.method =="POST":
		form = VendorForm(request.POST,request.FILES,instance=Vendor) 
		if form.is_valid():
			instance = form.save()
			instance.user = request.user
			#instance.secretKey = secret_code()
			instance.save()
			return redirect('vendor:vendor_account')
	else:
		form = VendorForm()
	context['form'] = form
	return render(request,'index/form.html',context)

@login_required(login_url="account:google_login")
def welcome_remarks(request):

	context = {}

	if request.is_ajax() and request.GET.get('pops'):#Popups/needed items ajax
		popups_advert(request,context)
		html = render_to_string('index/selected_place_order.html',context,request=request)
		return JsonResponse({'data':html})

	cart_count(request.user,context)
	context['vendor_account'] = "Useful"


	profile = vendor.objects.get(user=request.user)
	context['profile'] = profile

	return render(request,'vendor/vendor.html',context)

@login_required(login_url="account:google_login")
def vendor_account(request):
	context = {}
	#vendor_account(context,request)
	context['vendor_account'] = "Useful"
	context['title'] = "Vendor account"

	context['rate'] = vendor_bill_plan.objects.all().last()
	item_sold = OrderItem.objects.filter(vendor=request.user)
	item_sold_number = []
	for item in item_sold:
		if item.cart.being_delivered == False and item.cart.ordered==True:
			item_sold_number.append(item)
			context['item_sold'] = len(item_sold_number) 

	try:
		count = product.objects.filter(user=request.user).count()
		context['count'] = count
	except product.DoesNotExist:
		context['count'] = 0

	try:
		user_bill = BillPlan.objects.get(user=request.user)
		context['user_bill'] = user_bill
	except BillPlan.DoesNotExist:
		pass

	cart_count(request.user,context)
	context['categories'] = Categories.objects.all()


	if request.is_ajax() and request.GET.get('pops'):#Popups/needed items ajax
		popups_advert(request,context)
		html = render_to_string('index/selected_place_order.html',context,request=request)
		return JsonResponse({'data':html})

	elif request.is_ajax():#de-activating vendor account after 30 days

		data_id = request.GET.get('data')

		vendor_id = BillPlan.objects.get(id=data_id)
		vendor_id.due_date = None
		vendor_id.actived  = False
		vendor_id.item_num2 = 0
		vendor_id.save()

		try:#activating product-paid field after paying bill
			user_itmes = product.objects.filter(user=vendor_id.user)
			if user_itmes:
				user_itmes.update(Paid=False)
		except product.DoesNotExist:
			pass

	try:
		profile = vendor.objects.get(user=request.user)
		context['profile'] = profile
	except vendor.DoesNotExist:
		return redirect('index:index')

	if request.session.has_key('vendor_error'):
		context['vendor_error'] = request.session['vendor_error']
		del request.session['vendor_error']

	return render(request,'vendor/vendor_account.html',context)

@login_required(login_url="account:google_login")
def items_sold(request):

	context = {}

	if request.is_ajax() and request.GET.get('pops'):#Popups/needed items ajax
		popups_advert(request,context)
		html = render_to_string('index/selected_place_order.html',context,request=request)
		return JsonResponse({'data':html})

	elif request.is_ajax():
		context['rate'] = vendor_bill_plan.objects.all().last()
		
		try:#getting area agents
			agent = agent_info.objects.filter(district__icontains=vendor.objects.get(user=request.user).district)
			context['agents'] = agent
		except agent_info.DoesNotExist:
			pass

		item_to_deliver = OrderItem.objects.filter(vendor=request.user)
		context['item'] = item_to_deliver
		
		html = render_to_string('vendor/item_sold.html',context,request=request)
		return JsonResponse({'data':html})

@login_required(login_url="account:google_login")
def billPayment(request,plan=None):
	context = {}

	cart_count(request.user,context)
	#vendor_account(context,request)#'dict' object has no attribute 'user'

	context['title'] = plan + " " + "plan"

	plan_p = vendor_bill_plan.objects.all().last()#getting plan price that will be displayed to HTML template
	context['phone_number'] = plan_p
	if plan == "silver":
		context['price'] = plan_p.silver
	elif plan == "gold":
		context['price'] = plan_p.gold
	else:
		context['price']  = plan_p.platinum

	try:
		paid_bill = BillPlan.objects.get(user = request.user)#if user paid before/editing
	except  BillPlan.DoesNotExist:
		pass


	if request.method == "POST":

		if paid_bill:#if user is not making payment for first time
			form = billform(request.POST,instance=paid_bill)
		else:
			form = billform(request.POST)

		if form.is_valid():#free subscription is in account/view.py "bill view/function"
			instance = form.save(commit=False)
			instance.user = request.user
			instance.actived = False#activated not actived
			instance.plan = plan
			instance.item_num2 = 0
			instance.due_date = None# date will be added in verification view

			if plan =="Silver":
				instance.item_num = 20
			elif plan == "Gold":
				instance.item_num = 50
			else:
				instance.item_num = 100
			instance.save()

			return redirect('vendor:payment_feedback')
	else:
		form =  billform()

	context['form'] = form

	if request.is_ajax() and request.GET.get('pops'):#Popups/needed items ajax
		popups_advert(request,context)
		html = render_to_string('index/selected_place_order.html',context,request=request)
		return JsonResponse({'data':html})

	return render(request,"vendor/bill_plan.html",context)

@login_required(login_url="account:google_login")
def payment_feedback(request):
	context = {}

	cart_count(request.user,context)
	#vendor_account(context,request)#'dict' object has no attribute 'user'

	context['title'] = "paid"
	context['paid_bill'] = BillPlan.objects.get(user = request.user)

	if request.is_ajax() and request.GET.get('pops'):#Popups/needed items ajax
		popups_advert(request,context)
		html = render_to_string('index/selected_place_order.html',context,request=request)
		return JsonResponse({'data':html})

	return render(request,"vendor/thanks.html",context)

@login_required(login_url="account:google_login")
def bill_verification(request):
	context = {}
	context['title'] = "Verification"

	cart_count(request.user,context)
	#vendor_account(context,request)

	paid_bill = BillPlan.objects.all()
	context['bill'] = paid_bill


	if request.user.is_superuser:

		if request.is_ajax() and request.GET.get('pops'):
			pass
		
		elif request.is_ajax():
			current_date_time = datetime.datetime.now()#geting duedate after 30 days
			due_date_time = current_date_time + datetime.timedelta(days=30)

			bill_id = request.GET.get('data')
			selected_bill = BillPlan.objects.get(id = bill_id)
			selected_bill.actived =True
			selected_bill.due_date = due_date_time
			selected_bill.save()

			paid_bill = BillPlan.objects.all()
			context['bill'] = paid_bill

			try:#activating product-paid field after paying bill
				user_itmes = product.objects2.filter(user=selected_bill.user)

				if user_itmes:
					user_itmes.update(Paid=True)
			except product.DoesNotExist:
				pass

			html = render_to_string('vendor/bill_verification2.html',context,request=request)
			return JsonResponse({'data':html})
	else:
		return redirect('index:index')
	return render(request,"vendor/bill_verification.html",context)

@login_required(login_url="account:google_login")
def add_agent(request,id=None):
	context = {}
	context['title'] = "Add agent"

	if id:
		agent = agent_info.objects.get(id=id)

	if request.user.is_superuser:
		if request.method == "POST":
			if id:
				form = AgentForm(request.POST,request.FILES,instance=agent)
			else:
				form = AgentForm(request.POST,request.FILES)
			if form.is_valid():
				instance = form.save()
				instance.user = request.user
				instance.save()
				request.session['added_sucessfuly_msg'] = "Item added sucessfully!!"
				return redirect('account:dashboard')
		else:
			form= AgentForm()
		
	else:
		return redirect('index:index')

	context['form'] = form
	return render(request,'index/form.html',context)


@login_required(login_url="account:google_login")
def vendor_db(request):

	if request.user.is_superuser:

		context = {}
		cart_count(request.user,context)
		context['search_placeholder'] = "Search Vendor account name"
		context['title'] = "Vendor db"

		context['vendor_count'] = vendor.objects.all().count()
		context['active_account_count'] = BillPlan.objects.filter(actived=True).count()

		Vendor = vendor.objects.all().order_by('id')

		context['user_count'] = User.objects.all().count()

		query =request.GET.get('q')


		if query:
			context['title'] = query
			Vendor = Vendor.filter(Q(fullName__icontains=query)|
				                   Q(phoneWapNum__icontains=query)).distinct()

		page = request.GET.get('page', 1)
		paginator = Paginator(Vendor,12)

		try:
			Vendor = paginator.page(page)

		except PageNotAnInteger:
			Vendor = paginator.page(1)

		except EmptyPage:
			Vendor = paginator.page(paginator.num_pages)
		
		context['vendor'] = Vendor

	else:
		return redirect('index:index')

	return render(request,'vendor/vendor_db.html',context)


@login_required(login_url="account:google_login")
def deal_payment_verification(request):


	if request.user.is_superuser:
		context = {}
		context['title'] = "Deal Verification"
		context['deal_payment'] = deal_payment.objects.filter(Verified=False)


		if request.is_ajax() and request.GET.get('pops'):
			pass

		elif request.is_ajax():

			data = request.GET.get('data')
			selected_deal_payment = deal_payment.objects.get(id=data)
			deal_period = selected_deal_payment.period
			new_price   = selected_deal_payment.new_item_price
			current_date_time = datetime.datetime.now()#geting duedate after 30 days
			due_date_time = current_date_time + datetime.timedelta(days=deal_period)

			selected_item = product.objects.get(id=selected_deal_payment.item_id)
			selected_item.new_price = new_price
			selected_item.timer = due_date_time 
			selected_item.save()

			selected_deal_payment.Verified = True
			selected_deal_payment.save()

			context['deal_payment'] = deal_payment.objects.filter(Verified=False)

			html = render_to_string('vendor/deal_verification2.html',context,request=request)
			return JsonResponse({'data':html})
		return render(request,'vendor/deal_payment_verification.html',context)
	else:
		return redirect('index:index')
