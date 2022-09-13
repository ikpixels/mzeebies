from django.shortcuts import render,redirect
from .models import Order,OrderItem,item_size_color
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.urls import reverse
from django.template.loader import render_to_string
from products.models import product,Categories,Brand
from django.conf import settings
from . forms import mobile_form
from index.snipt import cart_count,send_html_mail,vendor_account,secret_code,popups_advert
from django.contrib.auth.decorators import login_required
from paypal.standard.forms import PayPalPaymentsForm
from vendor.models import vendor_bill_plan
from . models import Mobile, Order,billing_address,shipping_address,Top_seller
#ikpixels.py-facilitator@gmail.com

#import stripe
#stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


def color_size_(Product,Cart,color=None,size=None):
    Item = OrderItem.objects.get(item=Product,cart=Cart)

    try:
        item = item_size_color.objects.filter(item=Item)

        if color and size == None:
            pro = item_size_color(item=Item,color=color)
            pro.save()
        
        elif size and color == None:
            pro = item_size_color(item=Item,size=size)
            pro.save()

        elif size and color:
            pro = item_size_color(item=Item,color=color,size=size)
            pro.save()

    except item_size_color.DoesNotExist:
        if color and size == None:
            item = item_size_color(item=Item,color=color)
            item.save()

        elif size and color == None:
            item = item_size_color(item=Item,size=size)
            item.save()

        elif size and color:
            item = item_size_color(item=Item,color=color,size=size)
            item.save()

#______________________________________________________________________
def get_user_cart(request):
    if request.user.is_authenticated and not request.user.is_anonymous:
        try:
            cart = Order.objects.get(user=request.user,ordered=False,paid_bill=False)

        except Order.DoesNotExist:
            cart = Order(user=request.user)
            cart.save()

    else:
        cart_id = request.session.get('cart_id')
        if not cart_id:
            cart = Order()
            cart.save()
        else:
            cart = Order.objects.get(id=cart_id)
    return cart

def shopingcart(request):
	pass

@login_required(login_url="account:google_login")
def add_to_cart(request,slug=None):

    context = {}

    query =request.GET.get('q')#query 
    if query:
        request.session['q'] = query
        return redirect("products:mainshop")


    if request.is_ajax() and request.GET.get('pops'):#Popups/needed items ajax
        pass
    elif request.is_ajax():

        order = get_user_cart(request)
        item = product.objects.get(slug=slug)

        top_seller = Top_seller(product=item)
        top_seller.save()

        try:
            cart_item = OrderItem.objects.get(item=item,cart=order,vendor=item.user)
            quantity = cart_item.quantity
            quantity += 1
            cart_item.quantity = quantity
            cart_item.save()

            Stock = item.stock # decreasing number of stock
            Stock -= 1
            item.stock = Stock
            item.save()

        except OrderItem.DoesNotExist:
            cart_item = OrderItem(cart=order,item=item,quantity=1,vendor=item.user)
            cart_item.save()

            Stock = item.stock # decreasing number of stock
            Stock -= 1
            item.stock = Stock
            item.save()

        color = request.GET.get('color')
        size  = request.GET.get('size')
        color_size_(item,order,color,size)

    return redirect('cart:cart_view')



@login_required(login_url="account:google_login")
def remove_cart(request, id):
    context ={}

    if request.is_ajax() and request.GET.get('pops'):#Popups/needed items ajax
        pass
    if request.is_ajax():

        cart_item = OrderItem.objects.get(id=id)

        item = product.objects.get(slug=cart_item.item.slug)

        if cart_item.quantity > 1:

            try:
                color_size = item_size_color.objects.filter(item=cart_item).last()

                if color_size:
                    color_size.delete()

            except item_size_color.DoesNotExist:
                pass

            quantity = cart_item.quantity
            quantity -= 1
            cart_item.quantity = quantity
            cart_item.save()

            Stock = item.stock #stock increament
            Stock += 1
            item.stock = Stock
            item.save()

        else:
            try:
                color_size = item_size_color.objects.get(item=cart_item)

                if color_size:
                    color_size.delete()

            except item_size_color.DoesNotExist:
                pass

            cart_item.delete()

            Stock = item.stock #stock increament
            Stock += 1
            item.stock = Stock
            item.save()

        return redirect('cart:cart_view')

def cart_view(request):

    context = {}
    context['title'] = "Your shoping cart"
    context['brand'] = Brand.objects.all()
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


    if request.user.is_authenticated:
        order_ = get_user_cart(request)
        if order_:
            cart_count(request.user,context)

            query =request.GET.get('q')
            if query:
                request.session['q'] = query
                return redirect("products:mainshop")

            context['currency'] = Categories.objects.all().last()
            order = Order.objects.get(user = request.user,ordered=False,paid_bill = False)


            if order.checkout_stage == True  and order.pyment_method == "stripe" or order.paid_bill == True:
                request.session['finish_payment'] = "Finish your payment please"
                return HttpResponseRedirect(reverse('cart:stripe', args=[order.id]))
                del request.session['finish_payment'] 

            elif order.checkout_stage == True  and order.pyment_method == "paypal" or order.paid_bill == True:
                request.session['finish_payment'] = "Finish your payment please"
                return HttpResponseRedirect(reverse('cart:paypal', args=[order.id]))
                del request.session['finish_payment']

            context['order'] = order
        return render(request,'cart/cart.html',context)

    else:#for anonymous user
        request.session['user_error'] = "Your shoping cart is 0, Start shoping now !!"
        return redirect('products:mainshop')

@login_required(login_url="account:google_login")
def billing(request,id):
    context = {}
    context['title'] = "Checkout"
    cart_count(request.user,context)
    vendor_account(context,request)
   
    query =request.GET.get('q')
    if query:
        request.session['q'] = query
        return redirect("products:mainshop")

    cart = Order.objects.get(user=request.user,ordered=False,paid_bill=False)
    context['cart'] = cart


    if request.is_ajax() and request.GET.get('pops'):#Popups/needed items ajax
        popups_advert(request,context)
        html = render_to_string('index/selected_place_order.html',context,request=request)
        return JsonResponse({'data':html})

    elif request.is_ajax():
        #billing details__________________________
        first_name = request.GET.get('first_name')
        last_name  = request.GET.get('last_name')
        house  = request.GET.get('house')
        country= request.GET.get('country')
        town  = request.GET.get('town')
        suit  = request.GET.get('suit')
        zip_code= request.GET.get('zip')
        phone   = request.GET.get('phone')
        email   = request.GET.get('email')
        Billing = billing_address(user=request.user,
                     first_name=first_name,
                     last_name=last_name,
                     country=country,
                     city=town,
                     street_adress=house,
                     phone=phone,
                     email=email,
                     zip_code=zip_code,
                     apartment=suit).save()


        #shipping details___________________________
        first_name2 = request.GET.get('first_name2')
        last_name2= request.GET.get('last_name2')
        house2  = request.GET.get('house2')
        country2= request.GET.get('country2')
        town2  = request.GET.get('town2')
        suit2  = request.GET.get('suit2')
        zip_code2= request.GET.get('zip2')
        phone2   = request.GET.get('phone2')
        email2   = request.GET.get('email2')
        Billing=shipping_address(user=request.user,
                     first_name=first_name2,
                     last_name=last_name2,
                     country=country2,
                     city=town2,
                     street_adress=house2,
                     phone=phone2,
                     email=email2,
                     zip_code=zip_code2,
                     apartment=suit).save()

        
    return render(request,'cart/billing.html',context)

@login_required(login_url="account:google_login")
def paypal(request,id):
    context = {}

    cart_count(request.user,context)
    vendor_account(context,request)
    
    if request.session.has_key('finish_payment'):
        context['finish_payment'] = request.session['finish_payment']


    cart = Order.objects.get(user=request.user,id=id,ordered=False)
    cart.checkout_stage = True
    cart.pyment_method ="paypal"
    cart.save()

    context['cart'] = cart
    context['title'] = "paypal"
    context['USD'] = cart.USD

    host = request.get_host()
    paypal_dict ={'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount':cart.USD,
        'item_name':cart,
        'invoice': secret_code(),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('cart:paypal_thax')),
        'cancel_return': 'http://{}{}'.format(host, HttpResponseRedirect(reverse('cart:paypal', args=[cart.id]))),}
    paypal_form= PayPalPaymentsForm(initial=paypal_dict)
    context['paypal_form'] = paypal_form

    return render(request,'cart/paypal.html',context)

@login_required(login_url="account:google_login")
def stripe(request,id):#for mobile not stripe not stripe payment method

    context = {}
    
    context['title'] = "Mobile payment"
    context['phone_number'] = vendor_bill_plan.objects.all().last()
    cart_count(request.user,context)
    vendor_account(context,request)

    if request.session.has_key('finish_payment'):#(error msg)to avoid user adding item to basket befor completing transaction
        context['finish_payment'] = request.session['finish_payment']

    cart = Order.objects.get(user=request.user,id=id,ordered=False)
    cart.checkout_stage = True
    cart.pyment_method ="stripe"
    cart.save()

    context['cart'] = cart
    
    if request.method == "POST":

        form = mobile_form(request.POST)
        if form.is_valid():

            
            cart.paid_bill = True
            cart.save()
            
            instance = form.save(commit=False)
            instance.user = request.user
            instance.required = int(cart.get_total())
            instance.order = cart
            instance.save()
            return redirect('cart:charge')
    else:
        form = mobile_form()

    context['form'] = form
    return render(request,'cart/stripe.html',context)

@login_required(login_url="account:google_login")
def charge_d(request):# for mobile payment

    context = {}
    cart_count(request.user,context)
    vendor_account(context,request)


    if request.is_ajax() and request.GET.get('pops'):#Popups/needed items ajax
        popups_advert(request,context)
        html = render_to_string('index/selected_place_order.html',context,request=request)
        return JsonResponse({'data':html})

    elif request.is_ajax():#geting order detail
        id = request.GET.get('data')
        cart_ = Order.objects.filter(user=request.user).last()
        context['order'] = cart_

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

        html = render_to_string('cart/cart_detail2.html',context,request=request)
        return JsonResponse({'data':html})

    
    return render(request,'cart/mobile_thax.html',context)


@login_required(login_url="account:google_login")
def paypal_thax(request):
    context = {}
    cart_count(request.user,context)
    vendor_account(context,request)
    
    cart = Order.objects.filter(user=request.user).last()
    cart.ordered = True
    cart.paid_bill = True
    cart.ref_code = secret_code()
    cart.save()


    if request.is_ajax() and request.GET.get('pops'):#Popups/needed items ajax
        popups_advert(request,context)
        html = render_to_string('index/selected_place_order.html',context,request=request)
        return JsonResponse({'data':html})

    if request.is_ajax():
        id = request.GET.get('data')
        cart_ = Order.objects.filter(user=request.user).last()
        context['order'] = cart_

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

        html = render_to_string('cart/cart_detail2.html',context,request=request)
        return JsonResponse({'data':html})

    return render(request,'cart/paypal_thax.html',context)

@login_required(login_url="account:google_login")
def delivered(request):
    context = {}


    if request.is_ajax() and request.GET.get('pops'):#Popups/needed items ajax
        pass
    if request.is_ajax():
        data = request.GET.get('data')
        order = Order.objects.get(id=data,ordered=True)
        order.being_delivered = True
        order.save()
        context['orders'] = order
        html = render_to_string('cart/cart_detail.html',context,request=request)
        return JsonResponse({'data':html})

@login_required(login_url="account:google_login")
def confirm_mobile_payments(request,args=None):
    context = {}

    cart_count(request.user,context)
    vendor_account(context,request)

    if request.is_ajax() and request.GET.get('pops'):#Popups/needed items ajax
        popups_advert(request,context)
        html = render_to_string('index/selected_place_order.html',context,request=request)
        return JsonResponse({'data':html})
#_____________________ajax_________________________________________
    elif request.is_ajax():
        id_ = request.GET.get('data')

        post = Mobile.objects.get(id=id_)
        post.verify = True
        post.save()

        cart = Order.objects.get(id=post.order.id)
        cart.ordered = True
        cart.paid_bill = True
        cart.ref_code = secret_code()
        cart.save()

        payment = Mobile.objects.filter(mobile=post.mobile,verify=False)
        context['payment'] = payment

        html = render_to_string('cart/confirm_payment2.html',context,request=request)
        return JsonResponse({'data':html})
#_________________________________________________________________
    if args:
        if args == "airtel":
            context['title'] = "Airtel money"
        else:
            context['title'] = "TNM Mpamba"
        payment = Mobile.objects.filter(mobile=args,verify=False)
    else:
        context['title'] = "Payment Verification"
        payment = Mobile.objects.filter(verify=False)

    context['payment'] = payment
    return render(request,'cart/confirm_payment.html',context)