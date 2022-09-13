from django.db import models
#from django.contrib.contenttypes.fields import GenericRelation
#from star_ratings.models import Rating
import datetime
import uuid
from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_save
from django.urls import reverse
from django.utils.text import slugify
from django.dispatch import receiver
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating
from ckeditor.fields import RichTextField
from vendor.models import vendor
from index.snipt import get_date
#from djangoratings.fields import RatingField

class Paid_album_Manager(models.Manager):
	def get_queryset(self):
		allowed_album = super(Paid_album_Manager, self).get_queryset().filter(allowed=True)
		return allowed_album

class admin_album_Manager(models.Manager):
	def get_queryset(self):
		allowed_album = super(admin_album_Manager, self).get_queryset().filter(allowed=False)
		return allowed_album

class Album(models.Model):
	TYPE       = (('Album','Album'),('Riddim','Riddim'),('Single','Single'),('Cover','Cover'))
	vendor     = models.ForeignKey(vendor,null=True,blank=True,on_delete=models.CASCADE)
	artist     = models.CharField(max_length=500)
	title      = models.CharField(max_length=500)
	category   = models.CharField(max_length=500,choices=TYPE)
	first_artist  = models.BooleanField(default=False)
	slug          = models.SlugField(unique=True,null=True,blank=True,default=uuid.uuid1)
	file  = models.ImageField(upload_to='music/%y/%m/%d',blank=True)
	Paid           = models.BooleanField(default=False)
	allowed        = models.BooleanField(default=False)
	created_at     = models.DateTimeField(auto_now_add=True)
	updated_at     = models.DateTimeField(auto_now=True)
	ratings        = GenericRelation(Rating, related_query_name='item_rating')
	objects        = Paid_album_Manager()
	admin_album_objects = admin_album_Manager()

	def __str__(self):
		return self.title

	def whenpublished(self):
		post_date = get_date.post_time(self,self.created_at)
		return post_date

	def get_absolute_url(self):
		return reverse('music:album_list_detail',kwargs ={'slud':self.slug})

def create_album_slug(instance,new_slug=None):

	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug

	qs = Album.admin_album_objects.filter(slug=slug).order_by('-id')

	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug,qs.first().id)
		return create_album_slug(instance,new_slug=new_slug)
	return slug

def pre_save_receiver_album(sender,instance,*args,**kwargs):
	if not instance.slug:
		instance.slug = create_album_slug(instance)
pre_save.connect(pre_save_receiver_album,sender=Album)
#________________________________________________________________________

def upload_audio_location(instance,filename):
	basename,extension =filename.split('.mp3')
	return "%s/%s_%s_%s_%s.%s"%( 'Audio','MzeeBies.com',instance.title,'by',instance.artist,'.mp3')

CATEGORY    = ( ('House','House'),
		        ('Hip Hop','Hip hop'), 
		        ('Trap','Trap'),
		        ('Raggie','Raggie'),
		        ('Amapiano','Amapiano'),
		        ('Gospel','Gospel'),
		        ('Beats','Beats'),
		        ('Afro House','Afro House'),
		        ('Dancehall','Dancehall'),
		        ('Poetry','Poetry/Poem'),
		    )
class Paid_music_Manager(models.Manager):
	def get_queryset(self):
		allowed_music = super(Paid_music_Manager, self).get_queryset().filter(allowed=True)
		return allowed_music

class admin_music_Manager(models.Manager):
	def get_queryset(self):
		Not_allowed_music = super(admin_music_Manager,self).get_queryset().filter(allowed=False)
		return Not_allowed_music

class Music(models.Model):
	user       = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
	album      = models.ForeignKey(Album,null=True,blank=True,on_delete=models.CASCADE,related_name="album")    
	genre      = models.CharField(max_length=100,choices=CATEGORY)
	title      = models.CharField(max_length=500)
	sell       = models.BooleanField(default=False)
	price      = models.DecimalField(max_digits=18, decimal_places=2,null=True,blank=True)
	view       = models.PositiveIntegerField(default=0)
	topSeller  = models.PositiveIntegerField(default=0)
	artist     = models.CharField(max_length=500,null=True,blank=True)
	first_artist  = models.BooleanField(default=False)
	vote       = models.PositiveIntegerField(default=0)#downloads not vote
	slug           = models.SlugField(unique=True,null=True,blank=True,default=uuid.uuid1)
	Dicription     = RichTextField(null=True,blank=True)
	free_music     = models.BooleanField(default=False)
	file           = models.ImageField(upload_to='music/%y/%m/%d',blank=True,)
	mp3            = models.FileField(upload_to=upload_audio_location,blank=True,) 
	video          = models.URLField(null=True,blank=True)
	created_at     = models.DateTimeField(auto_now_add=True)
	updated_at     = models.DateTimeField(auto_now=True)
	Paid           = models.BooleanField(default=False)
	allowed        = models.BooleanField(default=False)
	rejected       = models.BooleanField(default=False)
	ratings        = GenericRelation(Rating, related_query_name='item_rating')
	objects        = Paid_music_Manager()
	admin_music_objects = admin_music_Manager()
	

	def __str__(self):
		return self.title


	def split_link(self):
		link = self.video
		youtube,Id = link.split('?v=')
		final_link = "https://www.youtube.com/embed/" + Id
		return final_link

	def whenpublished(self):

		post_date = get_date.post_time(self,self.created_at)
		return post_date

	def get_absolute_url(self):
		return reverse('music:music_detail',kwargs ={'slud':self.slug})

def create_slug(instance,new_slug=None):

	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug

	qs = Music.admin_music_objects.filter(slug=slug).order_by('-id')

	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug,qs.first().id)
		return create_slug(instance,new_slug=new_slug)
	return slug

def pre_save_receiver(sender,instance,*args,**kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)
pre_save.connect(pre_save_receiver,sender=Music)
#________________________________________________________________________

CATEGORY_2    = ( ('Agriculture','Agriculture'),
		        ('Intertainment','Intertainment'), 
		        ('Food and Nutritions','Food and Nutritions'),
		        ('Business','Business'),
		        ('Others','Others'),)

class Youtubefeed(models.Model):
	user       = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
	title      = models.CharField(max_length=500)
	video      = models.URLField()
	category   = models.CharField(max_length=100,choices=CATEGORY_2,default='Others')
	Paid           = models.BooleanField(default=False)
	created_at     = models.DateTimeField(auto_now_add=True)
	updated_at     = models.DateTimeField(auto_now=True)
	allowed        = models.BooleanField(default=False)

	def __str__(self):
		return self.title

	def split_link(self):
		link = self.video
		youtube,Id = link.split('?v=')
		final_link = "https://www.youtube.com/embed/" + Id
		return final_link