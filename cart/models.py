from django.db import models
from django.conf import settings
from products.models import product
from django.db.models.signals import post_save,pre_save
from django.urls import reverse
from django.utils.text import slugify
from django.dispatch import receiver
from vendor.models import vendor,vendor_bill_plan
#from djmoney.money import Money
#from djmoney.contrib.exchange.models import convert_money

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    checkout_stage  = models.BooleanField(default=False)
    paid_bill       = models.BooleanField(default=False)
    pyment_method   = models.CharField(max_length=50,blank=True)
    being_delivered = models.BooleanField(default=False)

    def __str__(self):
    	return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.cart.all():
            total += order_item.get_final_price()
        return total

    def USD(self):
        total = 0
        for order_item in self.cart.all():
            total += order_item.get_final_price_USD()
        return total

class OrderItem(models.Model):
    ordered  = models.BooleanField(default=False)
    color    = models.CharField(max_length=1000,blank=True,null=True)
    size     = models.CharField(max_length=1000,blank=True,null=True)
    cart     = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="cart")
    vendor   = models.CharField(max_length=1000,blank=True,null=True)
    item     = models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    received_from_vendor = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.item.item}"

    def vendor_number(self):
        vendor_num = vendor.objects.get(user=self.item.user).phoneWapNum
        code = (str(vendor_num)[:3])
        digits = (str(vendor_num )[3:])
        phone_number = "+" + "(" + code + ")" + " " + digits
        return phone_number

    def get_total_item_price(self):
        return self.quantity * self.item.price


    def get_item_price(self):
        if self.item.new_price:
            return self.item.new_price
        return self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.new_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.new_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

    def get_final_price_USD(self):
        USD =  740.256
        if self.item.new_price:
            return round((float(self.quantity) * float(self.item.new_price) * float(USD)),2)
        return round((float(self.quantity) * float(self.item.price) * float(USD)),2)

    def vendor_payment_contacts(self):
        Vendor_payment_info = vendor.objects.get(user=self.item.user)
        rate = vendor_bill_plan.objects.all().last()
        amount_to_be_paid = (float(rate.rate) * float(self.item.price))/100
        info = 'Amount : MKW ' + str(amount_to_be_paid) + ' || Mobile account name : ' +  str(Vendor_payment_info.mobile_payment_name) + ', phone # : ' + str(Vendor_payment_info.mobile_payment_no) + ' || ' + 'Bank name : ' +  str(Vendor_payment_info.bankAccType)+ ', Bank account name : ' +  str(Vendor_payment_info.bankAccName) + ', Bank account # : ' +  str(Vendor_payment_info.bankAccNumm)

        return info

class Top_seller(models.Model):
    product = models.ForeignKey(product,on_delete=models.CASCADE,related_name="top_seller")
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "top_seller"

@receiver(post_save,sender=Top_seller)
def add_top_seller(sender,created,instance,**kwargs):
    if created:
        instance.product.topSeller  += 1
        instance.product.save()

class item_size_color(models.Model):
    item  = models.ForeignKey(OrderItem,null=True, blank=True,on_delete=models.CASCADE,related_name="item_adds")
    color = models.CharField(max_length=500,null=True, blank=True,)
    size  = models.CharField(max_length=500,null=True, blank=True,) 


    def __str__ (self):
        return "size & color"

class billing_address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100,blank=True)
    last_name  = models.CharField(max_length=100,blank=True)
    country    = models.CharField(max_length=100,blank=True)
    city       = models.CharField(max_length=100,blank=True)
    street_adress = models.CharField(max_length=100,blank=True)
    phone      = models.CharField(max_length=100,blank=True)
    email      = models.CharField(max_length=100,blank=True)
    zip_code   = models.CharField(max_length=100,blank=True)
    apartment  = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

class shipping_address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100,blank=True)
    last_name  = models.CharField(max_length=100,blank=True)
    country    = models.CharField(max_length=100,blank=True)
    city       = models.CharField(max_length=100,blank=True)
    street_adress = models.CharField(max_length=100,blank=True)
    phone      = models.CharField(max_length=100,blank=True)
    email      = models.CharField(max_length=100,blank=True)
    zip_code   = models.CharField(max_length=100,blank=True)
    apartment  = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

class Mobile(models.Model):

    METHOD  = (('airtel','Airtel Money'),
               ('TNM','Mpamba')
               )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    mobile = models.CharField(max_length=600,choices=METHOD)
    name   = models.CharField(max_length=200) 
    order  = models.ForeignKey(Order,on_delete=models.CASCADE,related_name="mobile")
    rep_no = models.CharField(max_length=200) 
    required = models.DecimalField(max_digits=18, decimal_places=2,default=11)
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    verify = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.rep_no