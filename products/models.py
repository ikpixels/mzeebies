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
#from djangoratings.fields import RatingField


def upload_location2(instance,filename):
	basename,extension =filename.split('.')
	return "%s/%s.%s"%( 'banner',instance.image,extension)

class Categories(models.Model):
	user       = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
	category   = models.CharField(max_length=100)
	currency   = models.CharField(max_length=100,default="MWK")

	def __str__ (self):
		return self.category

class Brand(models.Model):
	brand      = models.CharField(max_length=100,default="Others")
	file2      = models.ImageField(upload_to="brand",blank=True,)
	

	def __str__ (self):
		return self.brand

class Paid_item_Manager(models.Manager):
	def get_queryset(self):
		paid_item = super(Paid_item_Manager, self).get_queryset().filter(Paid=True)
		return paid_item

class Non_Paid_item_Manager(models.Manager):
	def get_queryset(self):
		paid_item = super(Non_Paid_item_Manager, self).get_queryset().filter(Paid=False)
		return paid_item

class product(models.Model):
	user       = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE)
	vendor     = models.CharField(max_length=500,blank=True,null=True) #for easy querry    
	category   = models.ForeignKey(Categories,on_delete=models.CASCADE)
	category2  = models.CharField(max_length=500,blank=True,null=True)
	brand      = models.ForeignKey(Brand,on_delete=models.CASCADE,blank=True,null=True)
	brand2     = models.CharField(max_length=500,blank=True,null=True)
	item       = models.CharField(max_length=500)
	price      = models.DecimalField(max_digits=18, decimal_places=2)
	new_price  = models.DecimalField(max_digits=18,blank=True,null=True,decimal_places=2)
	stock      = models.PositiveIntegerField()
	view       = models.PositiveIntegerField(default=0)
	topSeller  = models.PositiveIntegerField(default=0)
	top_rated  = models.PositiveIntegerField(default=0)
	sizes      = models.CharField(max_length=1000,blank=True)
	color      = models.CharField(max_length=1000,blank=True)
	district       = models.CharField(max_length=1000,blank=True)
	area           = models.CharField(max_length=1000,blank=True)
	slug           = models.SlugField(unique=True,null=True,blank=True,default=uuid.uuid1)
	Dicription     = RichTextField(null=True,blank=True)
	allow_customer_buy_online = models.BooleanField(default=False)
	file           = models.ImageField(upload_to='kunsika/%y/%m/%d',blank=True,) 
	created_at     = models.DateTimeField(auto_now_add=True)
	updated_at     = models.DateTimeField(auto_now=True)
	Paid           = models.BooleanField(default=False)
	timer          = models.DateTimeField(auto_now_add=False, blank=True, null=True)
	ratings        = GenericRelation(Rating, related_query_name='item_rating')
	objects        = Paid_item_Manager()
	objects2        = Non_Paid_item_Manager()

	def __str__(self):
		return self.item


	def item_status(self):#To let customers know if item is new or uploaded today
		old_date = self.created_at
		old_date_ = str(old_date).split()[0]

		#JST = datetime.timezone(datetime.timedelta(hours=-2))

		current_date = datetime.datetime.today()
		current_date_= str(current_date).split()[0]

		if old_date_ == current_date_:
			status = "New"
		else:
			status = "Old"

		return status

	def vendor_phone_number(self):
		vendor_num = vendor.objects.get(user=self.user).phoneWapNum
		code = (str(vendor_num)[:3])
		digits = (str(vendor_num )[3:])
		phone_number = "+" + "(" + code + ")" + " " + digits
		return phone_number

	def discount(self):
		old_price = self.price
		new_price = self.new_price

		if new_price is  None:
			pass
		else:
			dis = (((new_price-old_price)/new_price)*100)
			return round(dis)

	

	def colors(self):
		if self.color:
			color = self.color.split(',')
			return color
		else:
			pass

	def item_sizes(self):
		if self.sizes:
			size = self.sizes.split(',')
			return size


	def get_absolute_url(self):
		return reverse('products:detail',kwargs ={'slud':self.slug})


class Popular(models.Model):
    product = models.ForeignKey(product,on_delete=models.CASCADE,related_name="popular")
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "views"

@receiver(post_save,sender=Popular)
def add_produc_views(sender,created,instance,**kwargs):
    if created:
        instance.product.view  += 1
        instance.product.save()

class add_image(models.Model):
	product = models.ForeignKey(product,on_delete=models.CASCADE,blank=True,null=True,related_name="image")
	file = models.ImageField(upload_to='kunsika/%y/%m/%d',blank=True,)

	def __str__(self):
		return "item"


class item_contacts(models.Model):
	phonenumber =  models.PositiveIntegerField()
	email       =  models.EmailField()

	def __str__(self):
		return "contacts"
		
def create_slug(instance,new_slug=None):

	slug = slugify(instance.item)
	if new_slug is not None:
		slug = new_slug

	qs = product.objects.filter(slug=slug).order_by('-id')

	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug,qs.first().id)
		return create_slug(instance,new_slug=new_slug)
	return slug

def pre_save_receiver(sender,instance,*args,**kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)
pre_save.connect(pre_save_receiver,sender=product)
#_________________________________________________________
def pre_save_category2(sender,instance,*args,**kwargs):
    if not instance.category2:
        instance.category2 = str(instance.category)

pre_save.connect(pre_save_category2,sender=product)
#__________________________________________________________
def pre_save_brand2(sender,instance,*args,**kwargs):
    if not instance.brand2:
        instance.brand2 = str(instance.brand)

pre_save.connect(pre_save_brand2,sender=product)
#__________________________________________________________

class category_banner(models.Model):
	Category       = models.ForeignKey(Categories,on_delete=models.CASCADE)
	Dicription     = models.TextField(blank=True)
	image          = models.ImageField(upload_to=upload_location2,blank=True,) 
	created_at     = models.DateTimeField(auto_now_add=True)
	updated_at     = models.DateTimeField(auto_now=True)

	def __str__ (self):
		return "category"

	def category_c(self):
		return str(self.Category)