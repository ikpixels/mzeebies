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
from vendor.models import vendor,BillPlan
from index.snipt import get_date
#from djangoratings.fields import RatingField

def upload_blog_location(instance,filename):
	basename,extension =filename.split('.')
	return "%s/%s.%s"%( 'ikpixels',instance.title,extension)

class Blog(models.Model):
	CATEGORY = (('Social Life','Social Life'),
		        ('Techinology','Techinology'),
		        ('Politics','Politics'),
		        ('Food','Food'),
		        ('Music','Music'),
		)
	user = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
	categorys = models.CharField(choices=CATEGORY,max_length=100)
	title = models.CharField(max_length=100)
	body = RichTextField()
	slug = models.SlugField(unique=True,blank=True,default=uuid.uuid1)
	comment_num = models.PositiveIntegerField(default =0)
	image  = models.ImageField(upload_to=upload_blog_location,blank=True,) 
	created_at     = models.DateTimeField(auto_now_add=True)
	updated_at     = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog:blog_detail',kwargs ={'slud':self.slug})

	def vendor(self):
		return vendor.objects.get(user=self.user)

	def whenpublished(self):

		post_date = get_date.post_time(self,self.created_at)
		return post_date


def create_slug(instance,new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Blog.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug,qs.first().id)
        return create_slug(instance,new_slug=new_slug)
    return slug

def pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_receiver,sender=Blog)





class comment(models.Model):
	blog = models.ForeignKey(Blog,null=True,blank=True,on_delete=models.CASCADE)
	full_name = models.CharField(max_length=100)
	body  = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.full_name

	def whenpublished(self):

		post_date = get_date.post_time(self,self.created_at)
		return post_date

def pre_save_receiver_comment_num(sender,instance,*args,**kwargs):
	slug_ = instance.blog.slug 
	blog_ = Blog.objects.get(slug=slug_)
	blog_.comment_num += 1
	blog_.save()

pre_save.connect(pre_save_receiver_comment_num,sender=comment)