from . models import Mobile,Order,OrderItem,item_size_color
from django.contrib.auth.models import User
from django.forms import ModelForm
from PIL import Image
from django import forms
from django.core.files import File


class mobile_form(ModelForm):
  class Meta:
    model = Mobile
    fields =['mobile','name','rep_no','amount']