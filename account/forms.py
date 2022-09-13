from django.forms import ModelForm
from django.contrib.auth.models import User
from PIL import Image
from django.contrib.auth.forms import UserCreationForm
from django.core.files import File
from image_cropping import ImageCropWidget
from django import forms
from django.core.files import File
#from django_countries import countries


#COUNTRY_CHOICES = ()

class user_creation_form(UserCreationForm):
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=True)
    last_name  = forms.CharField(required=True)
    phone_no   = forms.CharField(required=True)
    #country    = forms.CharField(default='Malawi' ,required=True)
    #district   = forms.CharField(required=True)
    #area   = forms.CharField(required=True)
    class Meta:
        model = User
        fields = ['first_name','last_name','phone_no','email','username','password1','password1']

        def save(self,commit=True):
            user = super(user_creation_form,self).save(commit=False)
            user.email =  self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.phone_no = self.cleaned_data['phone_no']
            #user.district = self.cleaned_data['district']
            #user.area = self.cleaned_data['area']
            #user.country = self.cleaned_data['country']

            if commit:
                user.save()
            return user