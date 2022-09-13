from . models import product,Brand,category_banner,add_image,Categories
from django.contrib.auth.models import User
from django.forms import ModelForm
from PIL import Image
from django import forms
from django.core.files import File
from ckeditor.widgets import CKEditorWidget


class deals_form(ModelForm):

  class Meta:
        model = product
        fields = ('new_price','timer')

        labels ={
                  'timer':'Enter end date and time for your deal(e.g yyyy-mm-dd h:m:s)',
                }


class ProductForm(ModelForm):

    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        Dicription = forms.CharField(widget=CKEditorWidget())
        model = product
        fields = ('item',
                  'category',
                  'brand',
                  'color',
                  'sizes',
                  'price',
                  'new_price',
                  'stock',
                  'Dicription',
                  'allow_customer_buy_online',
                  'file',
                  'x',
                  'y',
                  'width',
                  'height')
        labels ={
                  'color':'Available colors (OPTIONAL)',
                  'brand':'Item Brand(OPTIONAL)',
                  'price':'Old price',
                  'new_price':'New price(OPTIONAL)',
                  'sizes':'Available size (OPTIONAL)',
                  'Dicription':'Discription (OPTIONAL)',
                  'file':'Product image',
                }
        widgets = {
            'color': forms.TextInput(attrs={'placeholder': 'Separate item colors with comma e.g red,black,green'}),
            'sizes': forms.TextInput(attrs={'placeholder': 'Separate item size with comma e.g 2,5 or X,ML,M'}),
            'stock': forms.TextInput(attrs={'placeholder': 'Put zero if you dont want your customer to add this item to buskcate'}),
        }

    def save(self):
        photo = super(ProductForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.file)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((400,400), Image.ANTIALIAS)
        resized_image.save(photo.file.path)

        return photo

class EditProductForm(ModelForm):

  
    class Meta:
        Dicription = forms.CharField(widget=CKEditorWidget())
        model = product
        fields = ('item',
                  'category',
                  'brand',
                  'color',
                  'sizes',
                  'price',
                  'new_price',
                  'stock',
                  'Dicription',
                  'allow_customer_buy_online',
                 )
        labels ={
                  'color':'Available colors (OPTIONAL)',
                  'brand':'Item Brand(OPTIONAL)',
                  'price':'Old price',
                  'new_price':'New price(OPTIONAL)',
                  'sizes':'Available size (OPTIONAL)',
                  'Dicription':'Discription (OPTIONAL)',
                  
                }
        widgets = {
            'color': forms.TextInput(attrs={'placeholder': 'Separate item colors with comma e.g red,black,green'}),
            'sizes': forms.TextInput(attrs={'placeholder': 'Separate item size with comma e.g 2,5 or X,ML,M'}),
            'stock': forms.TextInput(attrs={'placeholder': 'Put zero if you dont want your customer to add this item to buskcate'}),
        }

   

class AddImageForm(ModelForm):

    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model  = add_image
        fields = ('file',
                  'x',
                  'y',
                  'width',
                  'height')
        labels ={
                  'file':'Product image',
                }
        widgets = {

        }

    def save(self):
        photo = super(AddImageForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.file)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((400,400), Image.ANTIALIAS)
        resized_image.save(photo.file.path)

        return photo

class ItemBanner(ModelForm):

    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = category_banner
        fields = ('Category',
                  'Dicription',
                  'image',
                  'x',
                  'y',
                  'width',
                  'height')
        labels ={
                  
                  'Dicription':'Discription (OPTIONAL)',
                }
        widgets = {}
            

    def save(self):
        photo = super(ItemBanner, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.image)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((1000, 600), Image.ANTIALIAS)
        resized_image.save(photo.image.path)

        return photo

class category_form(ModelForm):
  class Meta:
    model = Categories
    fields =['category']

class BrandForm(ModelForm):

    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Brand
        fields = ('brand',
                  'file2',
                  'x',
                  'y',
                  'width',
                  'height')
        labels ={}
        widgets = {}
            

    def save(self):
        photo = super(BrandForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.file2)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((250, 150), Image.ANTIALIAS)
        resized_image.save(photo.file2.path)

        return photo
