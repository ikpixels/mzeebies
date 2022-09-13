from django.shortcuts import render,redirect
from products.models import product,category_banner,Brand,Categories
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from . models import subscribe,place_order
from django.template.loader import render_to_string
from . forms import ItemNeededForm
from cart.models import OrderItem,Order
from .snipt import cart_count,send_html_mail,vendor_account,secret_code,popups_advert
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import resolve
from vendor.models import agent_info
from music.models import Music
import random
#from djmoney.money import Money
#from djmoney.contrib.exchange.models import convert_money

def index(request):
	context = {}

	context['home_image'] = "show_home_bacground_image"
	context['search_placeholder'] = "Search product based on name/your district/your area/Category/vendor/brand"

	category_list = []
	cate = Categories.objects.all()
	for category in cate:
		category_list.append(category)

	if category_list != []:
		selected_category = random.choice(category_list)
		context['selected_category'] = selected_category
		context['selected_item'] = product.objects.filter(category=selected_category)
		context['selected_item_count'] = product.objects.filter(category=selected_category).count()

	query =request.GET.get('q')
	
	if query:
		request.session['q'] = query
		return redirect("products:mainshop")

	cart_count(request.user,context)
	vendor_account(context,request)
	
	
	timer = product.objects.filter(timer__isnull=False)#deal list
	context['time'] = timer

	context['title']   = 'MzeeBies'#name of shop
	context['item1']   = product.objects.all().last()
	context['popular'] = product.objects.all().order_by('-view')
	context['item12']  = product.objects.all().order_by('-updated_at')
	context['item13']  = product.objects.all().first()
	context['banner']  = category_banner.objects.all()[:3]
	context['brand']   = Brand.objects.all().order_by('-id')

	tracks = Music.objects.all().order_by('-vote')
	context['track'] = tracks

	if request.is_ajax() and request.GET.get('pops'):
		popups_advert(request,context)
		html = render_to_string('index/selected_place_order.html',context,request=request)
		return JsonResponse({'data':html})

	elif request.is_ajax():
		category = request.GET.get('data');
		if category == 'Popular':
			context['popular'] = product.objects.all().order_by('-view')
			

		elif category == 'top_seller':
			context['popular'] = product.objects.all().order_by('-topSeller')
			
			
		else:
			context['popular'] = product.objects.filter(ratings__isnull=False).order_by('-ratings__average')

		html = render_to_string('index/top_seller.html',context,request=request)
		return JsonResponse({'data':html})
	
	return render(request,'index/index.html',context)

def contact(request):
	context = {}
	email_context = {}
	context['title'] = "Lets get in touch"
	
	cart_count(request.user,context)
	vendor_account(context,request)


	query =request.GET.get('q')
	context['search_placeholder'] = "Search product based on name/your district/your area/Category/vendor/brand"
	if query:
		request.session['q'] = query
		return redirect("products:mainshop")

	if request.is_ajax() and request.GET.get('pops'):#Popups/needed items ajax
		popups_advert(request,context)
		html = render_to_string('index/selected_place_order.html',context,request=request)
		return JsonResponse({'data':html})

	elif request.is_ajax():
		first_name = request.GET.get('first_name')
		last_name  = request.GET.get('last_name')
	
		email_context['msg'] = request.GET.get('msg')
		email_context['email'] = request.GET.get('phone')
		email_context['phone'] = request.GET.get('email')
		email_context['name'] =  first_name + " " + last_name
			
	return render(request,'index/contact.html',context)


def Subscribe(request):
	context ={}
	context2 ={}

	context2['msg'] = "Thanks for Subscribing"
	html = "index/subscribe_msg.html"

	email = request.GET['email']

	try:
		mail = subscribe.objects.filter(email=email)

		if mail:
			info ="false"
		else:
			subs = subscribe(email=email)
			subs.save()
			info ="true"
			#send_html_mail(email,"ikpixels.py@gmail.com",'Subscribe',html,context2)

	except subscribe.DoesNotExist:
		pass
	return JsonResponse({'data':info})
	

def unsubscribe(request):
	context ={}
	context2 = {}

	email = request.GET['email']

	context2['msg'] = "Thank you for unsubscribing"
	#context2['current_url'] = resolve(request.path_info).url_name


	try:
		mail = subscribe.objects.get(email=email)

		if mail:
			mail.delete()
			info = "true"

			html = "index/subscribe_msg.html"
			#send_html_mail(email,"ikpixels.py@gmail.com",'unsubscribe',html,context2)
		else:
			info ="false"

	except subscribe.DoesNotExist:
		info ="false"
		

	return JsonResponse({'data':info})

def terms_conditions(request):
	context  = {}
	context['title'] = "Terms & conditions"
	cart_count(request.user,context)


	if request.is_ajax() and request.GET.get('pops'):
		popups_advert(request,context)
		html = render_to_string('index/selected_place_order.html',context,request=request)
		return JsonResponse({'data':html})

	query =request.GET.get('q')
	context['search_placeholder'] = "Search product based on name/your district/your area/Category/vendor/brand"
	if query:
		request.session['q'] = query
		return redirect("products:mainshop")

	return render(request,'index/terms.html',context)

def about(request):
	context = {}
	context['title'] = "About us"
	cart_count(request.user,context)
	context['agents'] = agent_info.objects.all()
	vendor_account(context,request)

	query =request.GET.get('q')
	context['search_plac eholder'] = "Search product based on name/your district/your area/Category/vendor/brand"
	if query:
		request.session['q'] = query
		return redirect("products:mainshop")

	if request.is_ajax() and request.GET.get('pops'):
		popups_advert(request,context)
		html = render_to_string('index/selected_place_order.html',context,request=request)
		return JsonResponse({'data':html})

	elif request.is_ajax():# ORDER TAKING DATA from placing order form

		name  = request.GET.get('name')
		phone  = request.GET.get('phone')
		location  = request.GET.get('location')
		item  = request.GET.get('item')
		budget  = request.GET.get('budget')
		category_a  = request.GET.get('category')

		if budget == 0:
			budget2 = ''
		else:
			budget2  = budget

		order = place_order(name=name,
			                location=location,
			                phone=phone,
			                budget=budget2,
			                item2=item,
			                category = category_a,
			                orderNo=secret_code())
		order.save()

		html = render_to_string('index/place_order_feedback.html',context,request=request)
		return JsonResponse({'data':html})


	return render(request,'index/about.html',context)


def place_order_list(request,CATE = None):

	context = {}
	cart_count(request.user,context)
	vendor_account(context,request)

	context['categories'] = Categories.objects.all()

	if request.is_ajax() and request.GET.get('pops'):
		pass

	if CATE:#for category query
		context['title'] = CATE + " || Needed"
		Place_order = place_order.objects.filter(view=True,Type='Needed',category=CATE).order_by('-updated_at')
	else:
		context['title'] = "Needed item/s"
		Place_order = place_order.objects.filter(view=True,Type='Needed').order_by('-updated_at')

	query =request.GET.get('q')

	context['search_placeholder'] = "Search needed item/s"
	
	if query:
		context['title'] = query + " || Needed"
		Place_order =Place_order.filter(Q(item__icontains=query)|
		                  Q(item2__icontains=query)|
		                  Q(location__icontains=query)|
		                  Q(orderNo__icontains=query)|
		                  Q(category__icontains=query)|  
			              Q(budget__icontains=query)).distinct()


	page = request.GET.get('page', 1)
	paginator = Paginator(Place_order,12)

	try:
		Place_order = paginator.page(page)
	except PageNotAnInteger:
		Place_order = paginator.page(1)
	except EmptyPage:
		Place_order = paginator.page(paginator.num_pages)


	context['order'] = Place_order


	if request.is_ajax() and request.GET.get('pops'):
		popups_advert(request,context)
		html = render_to_string('index/selected_place_order.html',context,request=request)
		return JsonResponse({'data':html})


	return render(request,'index/needed_items.html',context)


@login_required(login_url="account:google_login")
def main_needed_item_view(request):

	if request.user.is_superuser:

		context = {}

		context['title'] = "Needed items"
		cart_count(request.user,context)
		vendor_account(context,request)


		Place_order = place_order.objects.filter(view=False)

		query =request.GET.get('q')


		context['search_placeholder'] = "Search needed item/s"

		if query:

			context['title'] = query + " || Needed"

			Place_order =Place_order.filter(Q(item__icontains=query)|
		                  Q(item2__icontains=query)|
		                  Q(location__icontains=query)|
		                  Q(orderNo__icontains=query)|
		                  Q(orderNo__icontains=query)|
		                  Q(category__icontains=query)|  
			              Q(budget__icontains=query)).distinct()


		page = request.GET.get('page', 1)

		paginator = Paginator(Place_order,12)

		try:

			Place_order = paginator.page(page)

		except PageNotAnInteger:

			Place_order = paginator.page(1)

		except EmptyPage:
			Place_order = paginator.page(paginator.num_pages)

		context['order'] = Place_order

		return render(request,'index/main_needed_items.html',context)
	else:
		return redirect('index:index')


@login_required(login_url="account:google_login")
def edit_needed_item_form(request,id=None):

	if request.user.is_superuser:

		context = {}

		context['title'] = "Edit needed item"
		cart_count(request.user,context)
		vendor_account(context,request)


		item = place_order.objects.get(id=id)

		if request.is_ajax() and request.GET.get('pops'):
			pass

		if request.method == "POST":

			form = ItemNeededForm(request.POST,request.FILES,instance=item)

			if form.is_valid():
				instance = form.save()
				instance.view = True
				instance.save()

				return redirect('index:main_needed_item_view')

		else:
			form  = ItemNeededForm()

		context['form'] = form

		return render(request,'index/form.html',context)
	else:
		return redirect('index:index')