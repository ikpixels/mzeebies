from django.shortcuts import render,redirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from index.snipt import cart_count,send_html_mail,vendor_account,secret_code,popups_advert

def help(request):
	context = {}
	context['title'] = "Help and support"
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

	return render(request,'help/help.html',context)
