from . models import Blog
from django.contrib.auth.models import User
from django.forms import ModelForm
from PIL import Image
from django import forms
from django.core.files import File
from ckeditor.widgets import CKEditorWidget

class BlogForm(ModelForm):

    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        body = forms.CharField(widget=CKEditorWidget())
        model = Blog
        fields = ('title',
                  'categorys',
                  'body',
                  'image',
                  'x',
                  'y',
                  'width',
                  'height')
        labels ={
                  
                 
                }
        widgets = {}
            

    def save(self):
        photo = super(BlogForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.image)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((1000, 600), Image.ANTIALIAS)
        resized_image.save(photo.image.path)

        return photo