from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from cart.models import OrderItem
from index.snipt import cart_count
from vendor.models import vendor,BillPlan
from . forms import BlogForm
from index.snipt import cart_count,send_html_mail,vendor_account,secret_code,popups_advert
from . models import Blog,comment


def blog(request,cate=None):#cate = blog Category

	context = {}

	if request.session.has_key('added_sucessfuly_msg'):
		context['added_sucessfuly_msg'] = request.session['added_sucessfuly_msg']
		del request.session['added_sucessfuly_msg']

	cart_count(request.user,context)
	vendor_account(context,request)
	
	if cate:
		context['title'] = cate
		blog = Blog.objects.filter(categorys=cate).order_by('-updated_at')
	else:
		context['title'] = "Blog"
		blog = Blog.objects.all()

	query =request.GET.get('q')
	context['search_placeholder'] = "Search blog"
	if request.session.has_key('q'):
		quer = request.session['q']
		context['title'] = quer 
		blog = blog.filter(Q(title__icontains=quer)| 
			               Q(categorys__icontains=quer)).distinct().order_by('-updated_at')
		del request.session['q']

	if query:
		context['title'] = query
		blog =blog.filter(Q(categorys__icontains=query)| 
			              Q(title__icontains=query)).distinct().order_by('-updated_at')


	page = request.GET.get('page', 1)
	paginator = Paginator(blog,12)

	try:
		blog = paginator.page(page)
	except PageNotAnInteger:
		blog = paginator.page(1)
	except EmptyPage:
		blog = paginator.page(paginator.num_pages)

	context['blog'] = blog

	if request.is_ajax() and request.GET.get('pops'):#Popups/needed items ajax
		popups_advert(request,context)
		html = render_to_string('index/selected_place_order.html',context,request=request)
		return JsonResponse({'data':html})

	return render(request,'blog/blog.html',context)

def blog_detail(request,slug):

	context = {}
	cart_count(request.user,context)
	vendor_account(context,request)
	context['title'] = "Blog Detail"

	query =request.GET.get('q')
	context['search_placeholder'] = "Search blog"
	if query:
		request.session['q'] = query
		return redirect("blog:blog")

	blog = Blog.objects.get(slug=slug)
	context['blog'] = blog

	context['related'] = Blog.objects.filter(Q(title__icontains=blog.title)|
			                                 Q(categorys=blog.title)).distinct()[:3]

	context['comment'] = comment.objects.filter(blog=blog)[:10]


	if request.is_ajax() and request.GET.get('pops'):#Popups/needed items ajax
		popups_advert(request,context)
		html = render_to_string('index/selected_place_order.html',context,request=request)
		return JsonResponse({'data':html})

	elif request.is_ajax():#getting comment data via ajax
	    name = request.GET.get('name')
	    body = request.GET.get('comment')
	    
	    comment_ = comment.objects.create(blog=blog,full_name=name,body=body)
	    comment_.save()

	    context['comment'] = comment.objects.filter(blog=blog)[:10]

	    html = render_to_string('blog/blog_comment.html',context,request=request)
	    return JsonResponse({'data':html})

	return render(request,'blog/blog_detail.html',context)

@login_required(login_url="account:google_login")
def AddBlog(request,slug=None):
	context = {}

	context['title'] = "Add Blog"
	cart_count(request.user,context)
	vendor_account(context,request)

	if slug:
		blog_ = Blog.objects.get(slug=slug)

	try:
		Vendor = vendor.objects.get(user=request.user)#getting Vendor full name
	except vendor.DoesNotExist:
		pass

	try:#for allowing user to add item if they  settle their bills
	    Paid_bill   = BillPlan.objects.get(user=request.user)
	    context['bill'] = Paid_bill

	    Num_of_item = Paid_bill.item_num
	    added_item  = Paid_bill.item_num2

	    if added_item < Num_of_item:

	    	if request.method =="POST":
	    		if slug:# for  editing item
	    			form = BlogForm(request.POST,request.FILES,instance=blog_) 
	    		else: # for new item entry
	    			form = BlogForm(request.POST,request.FILES)

	    		if form.is_valid():
	    			instance = form.save()
	    			instance.user = request.user
	    			instance.save()

	    			Paid_bill.item_num2 += 1
	    			Paid_bill.save()

	    			request.session['added_sucessfuly_msg'] = "Blog added successfuly"

	    			return redirect('blog:blog')
	    	else:
	    		form = BlogForm()

	    else:
	    	request.session['bill_expired'] = "Your items rich maxmum!!"
	    	return redirect('account:bill')

	except BillPlan.DoesNotExist:
		return redirect('account:bill')

	context['form'] = form

	return render(request,'index/form.html',context)
