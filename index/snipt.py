from cart.models import OrderItem,Order
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.urls import reverse
from django.template.loader import render_to_string
from products.models import product,Popular,Categories,category_banner,Brand,item_contacts
import math
import random 
import string
from datetime import date
import datetime
from vendor.models import vendor


from . models import place_order

from django.utils import timezone
from django.conf import settings



from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
#from django.shortcuts import render,redirect


def popups_advert(request,context):#geting popup data randomly

	order_list = []

	try:
		Place_order = place_order.objects.all().order_by('-updated_at')
		for order in Place_order:
			order_list.append(order.id)

		if order_list !=  []:
			selected_orderId = random.choice(order_list)
			order_choice = place_order.objects.get(id=selected_orderId,view=True)
			context['selected_place_order'] = order_choice

	except place_order.DoesNotExist:
		pass


def vendor_account(context,request):

	if request.user.is_authenticated and not request.user.is_anonymous:
		try:
			profile_ = vendor.objects.get(user=request.user)
			if profile_:
				context['vendor_account'] = profile_
		except vendor.DoesNotExist:
			pass


def cart_count(request,context):# for cart count , random selection of place order list and ads popup

	#____________________________order category option list

	try:
		options = Categories.objects.all()
		context['options'] = options

	except Categories.DoesNotExist:
		pass

	#____________________________cart count

	if request.is_authenticated:

		try:
			order = Order.objects.filter(user=request,paid_bill=False).last()
			context['cart_count'] = OrderItem.objects.filter(cart=order).count()
		except Order.DoesNotExist:
			context['cart_count'] = 0
	else:
		context['cart_count'] = 0

def secret_code():
	date_str = date.today().strftime('%Y%m%d')[2:] + str(datetime.datetime.now().second)
	rand_str = "".join([random.choice(string.digits) for count in range (3)])
	return date_str + rand_str


def added_sucessfully_msg(request,context):
	if request.session.has_key('added_sucessfuly_msg'):
		context['added_sucessfuly_msg'] = request.session['added_sucessfuly_msg']
		del request.session['added_sucessfuly_msg']


def send_html_mail(to_,from_,subject_,template,context):

	subject, from_email, to = subject_, from_, to_
	html_content = render_to_string(template,context) # render with dynamic value
	text_content = strip_tags(html_content) # Strip the html tag. So people can see the pure text at least.

	# create the email, and attach the HTML version as well.
	msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
	msg.attach_alternative(html_content, "text/html")
	msg.send()

class get_date:
	def post_time(self,post_date):

		now = timezone.now()

		diff= now - post_date

		if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:

			seconds= diff.seconds

			if seconds == 1:
				return str(seconds) +  "second ago"

			else:
				return str(seconds) + " seconds ago"


		if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
			minutes= math.floor(diff.seconds/60)

			if minutes == 1:
				return str(minutes) + " minute ago"

			else:
				return str(minutes) + " minutes ago"


		if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:

			hours= math.floor(diff.seconds/3600)

			if hours == 1:

				return str(hours) + " hour ago"


			else:
				return str(hours) + " hours ago"

        # 1 day to 30 days
		if diff.days >= 1 and diff.days < 30:

			days= diff.days

			if days == 1:

				return str(days) + " day ago"

			else:
				return str(days) + " days ago"

		if diff.days >= 30 and diff.days < 365:
			months= math.floor(diff.days/30)


			if months == 1:
				return str(months) + " month ago"

			else:
				return str(months) + " months ago"

		if diff.days >= 365:

			years= math.floor(diff.days/365)

			if years == 1:
				return str(years) + " year ago"

			else:
				return str(years) + " years ago"

