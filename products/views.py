from django.shortcuts import render,redirect
from . forms import ProductForm,EditProductForm,deals_form,BrandForm,ItemBanner,AddImageForm,category_form
from . models import product,Popular,Categories,category_banner,Brand,item_contacts
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from cart.models import OrderItem
from index.snipt import cart_count,send_html_mail,vendor_account,added_sucessfully_msg,popups_advert
from vendor.models import vendor,BillPlan,vendor_bill_plan,agent_info
from vendor.forms import deal_payment_form


def user_location(context,request):#with vendor account
	if request.user.is_authenticated and not request.user.is_anonymous:

		try:
			area = vendor.objects.get(user=request.user)
			context['district'] = area.district
			context['area'] = area.area

		except vendor.DoesNotExist:
			pass

def main_shop(request,context,args_=None,args_2=None):
	context['categories'] = Categories.objects.all()


	if request.session.has_key('added_sucessfuly_msg'):
		context['added_sucessfuly_msg'] = request.session['added_sucessfuly_msg']
		del request.session['added_sucessfuly_msg']

	cart_count(request.user,context)
	vendor_account(context,request)
	user_location(context,request)#with vendor account
	
	context['brand'] = Brand.objects.all()

	if request.session.has_key('user_error'):#for anonymous user
		user_error = request.session['user_error']
		context['user_error'] = user_error
		del request.session['user_error']

	if args_:
		item = product.objects.filter(Q(brand2=args_)|
			                          Q(vendor=args_)|
			                          Q(area=args_)|
			                          Q(district=args_)|
			                          Q(category2=args_)).distinct().order_by('-updated_at')
		context['title'] = args_
		context['args'] = args_

	elif args_2 == 'Top_Seller':
		context['args'] = "Top Seller"
		context['title'] = "Top Seller"
		item = product.objects.all().order_by('-topSeller')

	elif args_2 == 'Item_Deals':
		deals_count = product.objects.filter(timer__isnull=False).count()
		context['args'] = "Deals" 
		context['title'] = "Deals"
		context['deals'] = "Display deals countdown"
		item = product.objects.filter(timer__isnull=False).order_by('-updated_at')

	elif args_2 == 'Top_rated':
		context['args'] = "Top Rated"
		context['title'] = "Top Rated"
		item = product.objects.filter(ratings__isnull=False).order_by('-ratings__average')

	elif args_2 == "Popular":
		context['title'] = "Popular"
		context['args'] = "Popular"
		item = product.objects.all().order_by('-view')

	else:
		context['title'] = "Products"
		context['args'] = "All"
		item = product.objects.all().order_by('-updated_at')

	query =request.GET.get('q')

	context['search_placeholder'] = "Search product based on name/your district/your area/Category/vendor/brand"
	if request.session.has_key('q'):
		quer = request.session['q']
		context['args'] = quer
		context['title'] = quer 
		item = item.filter(Q(item__icontains=quer)|
		                   Q(area__icontains=quer)|
		                   Q(vendor__icontains=quer)|
		                   Q(brand2__icontains=quer)|
		                   Q(district__icontains=quer)| 
			               Q(category2__icontains=quer)).distinct()
		del request.session['q']

	if query:
		context['args'] = query
		context['title'] = query
		item =item.filter(Q(item__icontains=query)|
		                  Q(area__icontains=query)|
		                  Q(vendor__icontains=query)|
		                  Q(brand2__icontains=query)|
		                  Q(district__icontains=query)|  
			              Q(category2__icontains=query)).distinct()


	page = request.GET.get('page', 1)
	paginator = Paginator(item,20)

	try:
		item = paginator.page(page)
	except PageNotAnInteger:
		item = paginator.page(1)
	except EmptyPage:
		item = paginator.page(paginator.num_pages)

	context['items']  = item

def mainshop(request,args_=None,args_2=None):
	context = {}
	main_shop(request,context,args_,args_2)
	vendor_account(context,request)

	if request.is_ajax() and request.GET.get('pops'):#Popups/needed items ajax
		popups_advert(request,context)
		html = render_to_string('index/selected_place_order.html',context,request=request)
		return JsonResponse({'data':html})

	return render(request,'products/shop.html',context)

@login_required(login_url="account:google_login")
def Deal_payment_form(request,slug):

	context = {}
	context['title'] = "Make deal"
	context['deal_price'] = vendor_bill_plan.objects.all().last()

	item = product.objects.get(slug=slug)
	context['item'] = item

	if request.method == "POST":

		form = deal_payment_form(request.POST)

		if form.is_valid():
			instance = form.save()
			instance.user = request.user
			instance.item_id  = item.id
			instance.save()

			request.session['added_sucessfuly_msg'] = "You have successfuly made a deal.Your payment will be verified soon!!"

			return HttpResponseRedirect(reverse('products:detail', args=[item.slug]))
	else:
		form = deal_payment_form()

	context['form'] = form
	return render(request,'products/deals_payment_form.html',context)

@login_required(login_url="account:google_login")
def additem(request,id,slug=None):

	context = {}

	context['title'] = "Add product"
	cart_count(request.user,context)
	vendor_account(context,request)

	if slug:
		USER = request.user
		location = vendor.objects.get(user=request.user)
	else:
		USER = vendor.objects.get(id=id).user
		location = vendor.objects.get(id=id)
		
	

	if slug:
		item = product.objects.get(slug=slug)

	try:
		Vendor = vendor.objects.get(user=USER)#getting Vendor full name
	except vendor.DoesNotExist:
		pass

	try:#for allowing user to add item if they  settle their bills
	    Paid_bill   = BillPlan.objects.get(user=USER)
	    context['bill'] = Paid_bill

	    Num_of_item = Paid_bill.item_num
	    added_item  = Paid_bill.item_num2

	    if added_item < Num_of_item or Paid_bill.due_date != None:

	    	if request.method =="POST":
	    		if slug:# for  editing item
	    			form = EditProductForm(request.POST,request.FILES,instance=item) 
	    		else: # for new item entry
	    			form = ProductForm(request.POST,request.FILES)
	    			
	    		if form.is_valid():
	    			instance = form.save()
	    			instance.user = USER
	    			instance.vendor = str(Vendor.fullName)
	    			instance.district = location.district
	    			instance.area = location.area
	    			instance.Paid = True
	    			instance.save()

	    			Paid_bill.item_num2 += 1
	    			Paid_bill.save()

	    			request.session['added_sucessfuly_msg'] = "Item added successfuly"

	    			return redirect('products:item_view')
	    	else:
	    		form = ProductForm()

	    else:
	    	request.session['bill_expired'] = "Your items rich maxmum!!"
	    	return redirect('account:bill')

	except BillPlan.DoesNotExist:
		return redirect('account:bill')

	context['form'] = form

	return render(request,'index/form.html',context)

@login_required(login_url="account:google_login")
def additem_msg(request):
	context = {}
	context['contacts_info'] = item_contacts.objects.all().last()
	context['agents'] = agent_info.objects.all()
	return render(request,'products/additem_msg.html.html',context)

@login_required(login_url="account:google_login")
def item_view(request):
	context = {}
	context['title'] = "Add addition image"
	cart_count(request.user,context)
	vendor_account(context,request)

	query =request.GET.get('q')
	context['search_placeholder'] = "Search product based on name/your district/your area/Category/vendor/brand"
	if query:
		request.session['q'] = query
		return redirect("products:mainshop")

	context['item']  = product.objects.all().last()
	return render(request,'products/item_view.html',context)

def detail(request,slug):
	context = {}

	context['brand'] = Brand.objects.all()
	context['categories'] = Categories.objects.all()

	if request.session.has_key('added_sucessfuly_msg'):
		context['added_sucessfuly_msg'] = request.session['added_sucessfuly_msg']
		del request.session['added_sucessfuly_msg']

	cart_count(request.user,context)
	vendor_account(context,request)
	user_location(context,request)#with vendor account
	
	query =request.GET.get('q')
	context['search_placeholder'] = "Search product based on name/your district/your area/Category/vendor/brand"
	if query:
		request.session['q'] = query
		return redirect("products:mainshop")

	item = product.objects.get(slug=slug)

	related = product.objects.filter(Q(item=item)| 
			                         Q(category=item.category)).distinct() 
	context['related'] = related
	context['r_count'] = related.count()

	context['vendor'] = vendor.objects.get(user=item.user)#getting vendor icon
	
	context['title'] =  item
	context['item'] = item

	popular = Popular(product=item)
	popular.save()

	if request.is_ajax() and request.GET.get('pops'):#Popups/needed items ajax
		popups_advert(request,context)
		html = render_to_string('index/selected_place_order.html',context,request=request)
		return JsonResponse({'data':html})

	return render(request,'products/detail.html',context)

def delete_item(request,slug):
	context = {}
	if request.is_ajax():

		item = product.objects.get(slug=slug)
		item.delete()

		main_shop(request,context)

		html = render_to_string('products/shop2.html',context,request=request)
		return JsonResponse({'data':html})
		


@login_required(login_url="account:google_login")
def additemBanner(request,args=None):
	context = {}

	cart_count(request.user,context)
	vendor_account(context,request)

	if args:
		data = category_banner.objects.get(id=args)
		context['title'] = "Edit banner"
	else:
		context['title'] = "Add category banner"

	if request.method =="POST":

		if args:
			form = ItemBanner(request.POST,request.FILES,instance=data)
		else:
			form = ItemBanner(request.POST,request.FILES)

		if form.is_valid():
			form.save()
			return redirect('products:category_v')
	else:
		form = ItemBanner()
	context['form'] = form
	return render(request,'index/form.html',context)

@login_required(login_url="account:google_login")
def additemImage(request,slug):
	context = {}

	context['title'] = "Add item image"
	cart_count(request.user,context)
	vendor_account(context,request)


	item = product.objects.get(slug=slug)

	if request.method =="POST":
		form = AddImageForm(request.POST,request.FILES) 
		if form.is_valid():
			instance = form.save()
			instance.product = item
			instance.save()
			return redirect('products:item_view')
	else:
		form = AddImageForm()
	context['form'] = form
	return render(request,'index/form.html',context)

@login_required(login_url="account:google_login")
def category_v(request):
	context = {}
	context['title'] = "Add category"
	cart_count(request.user,context)
	vendor_account(context,request)
	

	categ  = Categories.objects.all().order_by('id')
	context['categories'] = categ

	banner = category_banner.objects.all()[:3]
	context['banner'] = banner

	context['count'] = product.objects.all().count()

	if request.is_ajax():
		category = request.GET.get('category')
		cate = Categories(category=category)
		cate.save()

		categ  = Categories.objects.all().order_by('id')
		context['categories'] = categ

		html = render_to_string('products/category2.html',context,request=request)
		return JsonResponse({'data':html})

	return render(request,'products/category.html',context)

def upload_brand_img(request):
	context = {}

	brand = Brand.objects.all().order_by('-id')[:10]
	context['brand'] = brand

	context['title'] = "Add brand"

	if request.method == "POST":
		form = BrandForm(request.POST,request.FILES)
		if form.is_valid():
			instance = form.save()
			instance.user = request.user
			instance.save()
			return redirect('products:upload_brand')
	else:
		form = BrandForm()
	context['form'] = BrandForm()
	return render(request,'index/form.html',context)

def delete_brand(request,id):
	item = Brand.objects.get(id=id)
	item.delete()
	return redirect('products:mainshop')


def timer(request):
	context = {}

	if request.is_ajax():
		id_ = request.GET.get('data')
		item = product.objects.get(id=id_)
		item.timer = None
		item.new_price = None
		item.save()
		html = render_to_string('products/category2.html',context,request=request)
		return JsonResponse({'data':html})

def remove_category(request):
	context = {}
	if request.is_ajax():
		data = request.GET.get('data')


		cate1  = Categories.objects.get(id=data)
		cate1.delete()

		context['removed'] = 'Removed successfuly' 

		categ  = Categories.objects.all().order_by('id')
		context['categories'] = categ

		html = render_to_string('products/category2.html',context,request=request)
		return JsonResponse({'data':html})