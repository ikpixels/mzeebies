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

class subscribe(models.Model):
	email = models.EmailField()

	def __str__(self):
		return self.email


class place_order(models.Model):
	Type = models.CharField(max_length=100,default="Needed")
	name = models.CharField(max_length=100,null=True,blank=True)
	location = models.CharField(max_length=100,null=True,blank=True)
	phone  =  models.PositiveIntegerField(default=0,null=True,blank=True)
	budget =  models.DecimalField(max_digits=18, decimal_places=2,null=True,blank=True)
	item = models.CharField(max_length=100,null=True,blank=True)
	item2  = models.TextField(null=True,blank=True)
	category = models.CharField(max_length=100,null=True,blank=True)
	slug  = models.SlugField(unique=True,null=True,blank=True,default=uuid.uuid1)
	view  = models.BooleanField(default=False)
	find  = models.BooleanField(default=False)
	found = models.BooleanField(default=False)
	delivered = models.BooleanField(default=False)
	link      = models.URLField(null=True,blank=True)
	file      = models.ImageField(upload_to='kunsika/%y/%m/%d',blank=True,)
	created_at  = models.DateTimeField(auto_now_add=True)
	updated_at  = models.DateTimeField(auto_now=True)
	orderNo     = models.CharField(max_length=100,null=True,blank=True)


	def __str__(self):
		return self.name

def create_slug(instance,new_slug=None):

	slug = slugify(instance.orderNo)
	if new_slug is not None:
		slug = new_slug

	qs = place_order.objects.filter(slug=slug).order_by('-id')

	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug,qs.first().id)
		return create_slug(instance,new_slug=new_slug)
	return slug

def pre_save_receiver(sender,instance,*args,**kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)
pre_save.connect(pre_save_receiver,sender=place_order)
#__________________________________________________