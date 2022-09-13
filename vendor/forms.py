from . models import vendor,BillPlan,vendor_bill_plan,agent_info,deal_payment
from django.contrib.auth.models import User
from django.forms import ModelForm
from PIL import Image
from django import forms
from django.core.exceptions import ValidationError
from django.core.files import File
from products.models import product

	
class VendorForm(ModelForm):

    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = vendor
        fields = (
                  'fullName',
                  'phoneWapNum',
                  'Adress',
                  'district',
                  'area',
                  'mobile_payment_name',
                  'mobile_payment_no',
                  'bankAccType',
                  'bankAccName',
                  'bankAccBrach',
                  'bankAccNumm',
                  'file',
                  'x',
                  'y',
                  'width',
                  'height')
        labels ={
                  'fullName':'Full Name / Business Name',
                  'phoneWapNum':'Whatsapp Number(start with country code e.g 265993344416,start with 265 instead of 0 for Malawian Vendor)',
                  'bankAccName':'Bank Account Name',
                  'bankAccType':'Bank Name',
                  'bankAccBrach':'Bank Account Branch',
                  'bankAccNumm':'Bank Account Number',
                  'file':'Profile pic / Business logo',
                  'mobile_payment_name':'Name of your airtel money or mpamba account',
                  'mobile_payment_no':'number of your airtel money or mpamba account',
                }
        widgets = {
            }

    def clean(self):
      cleaned_data = super(VendorForm, self).clean()
      number = cleaned_data.get('phoneWapNum')

      if not str(number).startswith(u"265"):
          msg = "Must start with 265(or your country code for non Malawian)"
          self.add_error('phoneWapNum',msg)

      if len(str(number)) != 12:
          msg = "Your number must have 12 digits"
          self.add_error('phoneWapNum',msg)
      
      return cleaned_data


    def save(self):
        photo = super(VendorForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.file)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((400,400), Image.ANTIALIAS)
        resized_image.save(photo.file.path)

        return photo

class billform(ModelForm):
  class Meta:
    model = BillPlan
    fields =['name','payment_method','ref_code','price']
    labels ={
                  'name':'Full Name',
                  'ref_code':'Ref',
                  'price':'Amount',
                }
    

class bill_verification_form(ModelForm):
  class Meta:
    model = BillPlan
    fields =['due_date']
    labels ={
                  'due_date':'',
                  
                }

class AgentForm(ModelForm):

    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = agent_info
        fields = (
                  'title',
                  'first_name',
                  'last_name',
                  'phonenumber',
                  'email',
                  'district',
                  'area',
                  'adress',
                  'agent',
                  'file',
                  'x',
                  'y',
                  'width',
                  'height')
        labels ={
                }
        widgets = {
            }

    def clean(self):
      cleaned_data = super(AgentForm, self).clean()
      number = cleaned_data.get('phonenumber')

      if not str(number).startswith(u"265"):
          msg = "Must start with 265(or your country code for non Malawian)"
          self.add_error('phonenumber',msg)

      if len(str(number)) != 12:
          msg = "Your number must have 12 digits"
          self.add_error('phonenumber',msg)
      
      return cleaned_data


    def save(self):
        photo = super(AgentForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.file)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((400,400), Image.ANTIALIAS)
        resized_image.save(photo.file.path)

        return photo

class deal_payment_form(ModelForm):
  class Meta:
    model = deal_payment
    fields =['name','payment_method','ref_code','amount','period','new_item_price']
    labels ={
                  'name':'Full Name',
                  'ref_code':'Ref',
                  'period':'Number of days for deal.'
                }

  def clean(self):
      cleaned_data = super(deal_payment_form, self).clean()
      period = cleaned_data.get('period')
      amount = cleaned_data.get('amount')
    

      deal_charge = vendor_bill_plan.objects.all().last().deal_price * period

      if deal_charge != amount:
          msg = "Your required to pay" + " " +  str(deal_charge)
          self.add_error('amount',msg)


      
      return cleaned_data
    
 