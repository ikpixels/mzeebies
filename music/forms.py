from . models import Album,Music,Youtubefeed
from django.contrib.auth.models import User
from django.forms import ModelForm
from PIL import Image
from django import forms
from django.core.files import File
from ckeditor.widgets import CKEditorWidget



class AlbumForm(ModelForm):

    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        Dicription = forms.CharField(widget=CKEditorWidget())
        model = Album
        fields = ('artist',
                  'category',
                  'title',
                  'first_artist',
                  'file',
                  'x',
                  'y',
                  'width',
                  'height')
        labels ={
                  'file':'Cover artwork',
                  'title':'Album/track title',
                  'first_artist':'Click here if is this your first song/album'
                }
        widgets = {

        }

    def save(self):
        photo = super(AlbumForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.file)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((400,400), Image.ANTIALIAS)
        resized_image.save(photo.file.path)

        return photo

class MusicForm(ModelForm):

    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        Dicription = forms.CharField(widget=CKEditorWidget())
        model = Music
        fields = (
                  'title',
                  'genre',
                  'mp3',
                  'video',
                  'Dicription',
                  #'sell',
                  #'price',
                  'file',
                  'x',
                  'y',
                  'width',
                  'height')
        labels ={
                  'file':'Cover artwork',
                  'price':'Price(OPTIONAL)',
                  'video':'Enter youtube track video link here(OPTIONAL)',
                  'title':'Track title',
                  'sell ':'Sell online'
                }
        widgets = {
                'video': forms.TextInput(attrs={'placeholder': 'e.g https://www.youtube.com/watch?v=SVY8I46dkb0'}),
        }

    def save(self):
        photo = super(MusicForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.file)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((400,400), Image.ANTIALIAS)
        resized_image.save(photo.file.path)

        return photo


class youtubefeed_form(ModelForm):

  class Meta:
        model = Youtubefeed
        fields = ('title','category','video')

        labels ={
                  'video':'Enter youtube video link here',
                }
        widgets = {
            'video': forms.TextInput(attrs={'placeholder': 'e.g https://www.youtube.com/watch?v=SVY8I46dkb0'}),
  
        }



