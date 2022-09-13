from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
from django.urls import reverse
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.decorators import login_required
from . forms import AlbumForm,MusicForm,youtubefeed_form
from vendor.models import vendor
from products.models import product,category_banner,Brand,Categories 
from . models import Album,Music,Youtubefeed
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from vendor.models import vendor,BillPlan,vendor_bill_plan
from index.snipt import cart_count,send_html_mail,vendor_account,added_sucessfully_msg,popups_advert


def music(request,args_1=None,other_args=None):#music home page
	context = {}

	context['search_placeholder'] = "Search Music"
	context['music_image'] = "show_music_bacground_image"

	cart_count(request.user,context)
	vendor_account(context,request)
	context['popular'] = product.objects.all().order_by('-view')

	album = Album.objects.all()
	context['album'] = album

	youtubefeed = Youtubefeed.objects.all()
	context['youtubefeed'] = youtubefeed


	if other_args == "downloads":
		context['title'] = 'Most downloaded'
		tracks = Music.objects.all().order_by('-vote')

	elif other_args == 'Track Top 12':
		context['title'] = 'Top 12 | Most rated'
		tracks = Music.objects.filter(ratings__isnull=False).order_by('-ratings__average')

	elif other_args == 'New artist':
		context['title'] = 'New artist'
		tracks = Music.objects.filter(first_artist=True).order_by('-updated_at')

	elif args_1:
		context['title'] = args_1
		tracks = Music.objects.filter(genre=args_1).order_by('-updated_at')

	else:
		context['title'] = "Music"
		tracks = Music.objects.all().order_by('-updated_at')

	

	query =request.GET.get('q')

	if request.session.has_key('q'):
		quer = request.session['q']
		context['title'] = quer 

		tracks = tracks.filter(Q(title__icontains=quer)|
			                   Q(genre__icontains=quer)).distinct().order_by('-updated_at')
		del request.session['q']

	if query:
		context['title'] = query
		tracks = tracks.filter(Q(genre__icontains=query)|
			                   Q(title__icontains=query)).distinct().order_by('-updated_at')


	page = request.GET.get('page', 1)
	paginator = Paginator(tracks,12)

	try:
		tracks = paginator.page(page)
	except PageNotAnInteger:
		tracks = paginator.page(1)
	except EmptyPage:
		tracks = paginator.page(paginator.num_pages)

	context['tracks'] = tracks

	if request.is_ajax() and request.GET.get('pops'):#Popups/needed items ajax
		popups_advert(request,context)
		html = render_to_string('index/selected_place_order.html',context,request=request)
		return JsonResponse({'data':html})

	return render(request,'music/music.html',context)

def album_list(request,CATEGORY=None,TOP_TEN=None):
	context = {}
	context['music_image'] = "show_music_bacground_image"

	query =request.GET.get('q')

	if request.session.has_key('added_sucessfuly_msg'):
		context['added_sucessfuly_msg'] = request.session['added_sucessfuly_msg']
		del request.session['added_sucessfuly_msg']
	
	context['search_placeholder'] = "Search Album,Riddim,artist"
	context['popular'] = product.objects.all().order_by('-view')

	cart_count(request.user,context)
	vendor_account(context,request)

	youtubefeed = Youtubefeed.objects.all()
	context['youtubefeed'] = youtubefeed

	if CATEGORY =="Album":
		context['title'] = "Album list"
		album = Album.objects.filter(category="Album").order_by('-updated_at')
	elif CATEGORY == "Riddim":
		context['title'] = "Riddim list"
		album = Album.objects.filter(category="Riddim").order_by('-updated_at')
	elif TOP_TEN == "Album_top_12":
		context['title'] = "Album top 12"
		album = Album.objects.filter(category="Album",ratings__isnull=False).order_by('-ratings__average')
	elif TOP_TEN == "Cover_top_12":
		context['title'] = "Cover top 12"
		album = Album.objects.filter(category="Cover",ratings__isnull=False).order_by('-ratings__average')
	elif TOP_TEN == "Riddim_top_12":
		context['title'] = "Riddim top 12"
		album = Album.objects.filter(category="Riddim",ratings__isnull=False).order_by('-ratings__average')
	else:
		context['title'] = "Cover list"
		album = Album.objects.filter(category="Cover").order_by('-updated_at')


	if request.session.has_key('q'):
		quer = request.session['q']
		context['title'] = quer 

		album = album.filter(Q(title__icontains=quer)|
			                 Q(artist__icontains=quer)).distinct().order_by('-updated_at')
		del request.session['q']
    
	if query:
		context['title'] = query
		album = album.filter(Q(artist__icontains=query)|
			                 Q(title__icontains=query)).distinct().order_by('-updated_at')


	page = request.GET.get('page', 1)
	paginator = Paginator(album,12)


	try:
		album = paginator.page(page)
	except PageNotAnInteger:
		album = paginator.page(1)
	except EmptyPage:
		album = paginator.page(paginator.num_pages)

	context['album'] = album


	if request.is_ajax() and request.GET.get('pops'):#Popups/needed items ajax
		popups_advert(request,context)
		html = render_to_string('index/selected_place_order.html',context,request=request)
		return JsonResponse({'data':html})

	return render(request,'music/album_list.html',context)

def album_list_detail(request,slug=None,slug_2=None):

	context = {}
	context['music_image'] = "show_music_bacground_image"
	context['search_placeholder'] = "Search Music album"
	context['popular'] = product.objects.all().order_by('-view')

	if request.session.has_key('added_sucessfuly_msg'):
		context['added_sucessfuly_msg'] = request.session['added_sucessfuly_msg']
		del request.session['added_sucessfuly_msg']

	cart_count(request.user,context)
	vendor_account(context,request)

	youtubefeed = Youtubefeed.objects.all()
	context['youtubefeed'] = youtubefeed


	if slug_2:
		album = Album.admin_album_objects.get(slug=slug_2)
		context['title'] = album.title 
		context['album'] = album

		track = Music.admin_music_objects.filter(user=request.user,album=album)
		context['track'] = track

	else:
		album = Album.objects.get(slug=slug)
		context['title'] = album.title 
		context['album'] = album

		track = Music.objects.filter(album=album)
		context['track'] = track

	query =request.GET.get('q')
	context['search_placeholder'] = "Search Album,Riddim,artist"
	if query:
		request.session['q'] = query
		return redirect("music:music")

	try:
		get_rack_count = Music.admin_music_objects.filter(album=album).count()
	except Music.DoesNotExist:
		get_rack_count = Music.objects.filter(album=album).count()

	context['album_len'] = get_rack_count

	if request.is_ajax() and request.GET.get('pops'):#Popups/needed items ajax
		popups_advert(request,context)
		html = render_to_string('index/selected_place_order.html',context,request=request)
		return JsonResponse({'data':html})

	return render(request,'music/album_list_detail.html',context)

def music_detail(request,slug=None):

	context = {}
	context['music_image'] = "show_music_bacground_image"
	
	context['popular'] = product.objects.all().order_by('-view')

	cart_count(request.user,context)
	vendor_account(context,request)

	album = Album.objects.all()
	context['album'] = album

	youtubefeed = Youtubefeed.objects.all()
	context['youtubefeed'] = youtubefeed

	tracks = Music.objects.get(slug=slug)
	context['track'] = tracks

	context['title'] = tracks

	related =Music.objects.filter(Q(album=tracks.album)| 
			                             Q(genre =tracks.genre)).distinct()
	context['related_tracks'] = related

	query =request.GET.get('q')
	context['search_placeholder'] = "Search Music"
	if query:
		request.session['q'] = query
		return redirect("music:music")

	if request.is_ajax() and request.GET.get('pops'):#Popups/needed items ajax
		popups_advert(request,context)
		html = render_to_string('index/selected_place_order.html',context,request=request)
		return JsonResponse({'data':html})

	elif request.is_ajax():#downloads increments

		track_id = request.GET.get('data')
		tracks_d = Music.objects.get(id=track_id)
		
		current_downloads = tracks_d.vote
		current_downloads += 1
		tracks_d.vote = current_downloads 
		tracks_d.save()

	return render(request,'music/detail.html',context)

@login_required(login_url="account:google_login")
def create_album(request):
	context = {}
	context['music_image'] = "show_music_bacground_image"
	context['title'] = "Add album"

	cart_count(request.user,context)
	vendor_account(context,request)


	try:#for allowing user to add item if they  settle their bills
		Paid_bill   = BillPlan.objects.get(user=request.user)
		context['bill'] = Paid_bill

		Num_of_item = Paid_bill.item_num
		added_item  = Paid_bill.item_num2

		if added_item < Num_of_item:


			if request.method == "POST":

				form = AlbumForm(request.POST,request.FILES)

				if form.is_valid():
					instance = form.save()
					instance.vendor = vendor.objects.get(user=request.user)
					instance.save()

					Paid_bill.item_num2 += 1
					Paid_bill.save()

					return redirect('music:add_track')

			else:
				form = AlbumForm()

		else:
			request.session['bill_expired'] = "Your items rich maxmum!!"
			return redirect('account:bill')

	except BillPlan.DoesNotExist:
		return redirect('account:bill')

	context['form'] = form
	return render(request,'index/form.html',context)

@login_required(login_url="account:google_login")
def add_track(request,slug=None,edit_track_id=None):
	context = {}
	context['music_image'] = "show_music_bacground_image"
	context['title'] = "Add track/audio"

	cart_count(request.user,context)
	vendor_account(context,request)

	Vendor = vendor.objects.get(user=request.user)

	if slug:
		album = Album.admin_album_objects.get(slug=slug)
	else:
		album = Album.admin_album_objects.filter(vendor=Vendor).last()


	try:#for allowing user to add item if they  settle their bills
		Paid_bill   = BillPlan.objects.get(user=request.user)
		context['user_bill'] = Paid_bill

		Num_of_item = Paid_bill.item_num
		added_item  = Paid_bill.item_num2

		if added_item < Num_of_item:

			if request.method == "POST":

				if edit_track_id:

					track_to_edit = Music.objects.get(id=edit_track_id)

					track_to_edit.allowed = False
					track_to_edit.rejected = False
					track_to_edit.save()

					form = MusicForm(request.POST,request.FILES,instance=track_to_edit)
				else:
					form = MusicForm(request.POST,request.FILES)

				if form.is_valid():
					instance = form.save()
					instance.album = album 
					instance.first_artist = album.first_artist
					instance.artist = album.artist
					instance.user = request.user
					instance.save()

					if not edit_track_id:
						Paid_bill.item_num2 += 1
						Paid_bill.save()

					request.session['added_sucessfuly_msg'] = "Track added successfuly,We will allow our user to view/download your track after approving it"

					if album.category =="Single":
						return HttpResponseRedirect(reverse('music:user_music2', args=['Non proved song']))

					else:
						return HttpResponseRedirect(reverse('music:album_list_detail2', args=[album.slug])) 

			else:
				form = MusicForm()

		else:
			request.session['bill_expired'] = "Your items rich maxmum!!"
			return redirect('account:bill')

	except BillPlan.DoesNotExist:
		return redirect('account:bill')

	context['form'] = form

	return render(request,'index/form.html',context)

@login_required(login_url="account:google_login")
def main_music(request,args=None):

	if request.user.is_superuser:
		context = {}
		context['music_image'] = "show_music_bacground_image"

		if args == "Non approved track":
			context['title'] = "Non approved track/s"
			tracks = Music.admin_music_objects.filter(rejected=False).order_by('-updated_at')
			

		elif args == "Rejected track":
			context['title'] = "Rejected track/s"
			tracks = Music.admin_music_objects.filter(rejected=True).order_by('-updated_at')
			

		else:
			context['title'] = "Approved track/s"
			tracks = Music.objects.filter(allowed=True).order_by('-updated_at')


		query =request.GET.get('q')

		if query:
			context['title'] = query
			tracks = tracks.filter(Q(genre__icontains=query)|
			                       Q(title__icontains=query)).distinct().order_by('-updated_at')
			

		page = request.GET.get('page', 1)
		paginator = Paginator(tracks,12)

		try:
			tracks = paginator.page(page)
		except PageNotAnInteger:
			tracks = paginator.page(1)

		except EmptyPage:
			tracks = paginator.page(paginator.num_pages)

		context['tracks'] = tracks


		if request.is_ajax() and request.GET.get('pops'):
			pass
		elif request.is_ajax():#aprove music
			id_ = request.GET.get('data')
			data2 = request.GET.get('data2')
			aprove_music = Music.admin_music_objects.get(id=id_)

			try:
				aprove_album = Album.admin_album_objects.get(id=aprove_music.album.id)
				aprove_album.allowed = True
				aprove_album.save()

			except Album.DoesNotExist:
				pass


			if data2 =="approve":
				aprove_music.allowed = True# Approving track
				aprove_music.save()

			else:
				aprove_music.rejected = True #rejecting track
				aprove_music.save()

			tracks = Music.admin_music_objects.filter(rejected=False).order_by('-updated_at')
			context['tracks'] = tracks

			html = render_to_string('music/main_music2.html',context,request=request)
			return JsonResponse({'data':html})

	else:
		return redirect('index:index')

	return render(request,'music/main_music.html',context)

def paginator_for_track(track,request,context):

	if request.is_ajax() and request.GET.get('pops'):#Popups/needed items ajax
		popups_advert(request,context)
		html = render_to_string('index/selected_place_order.html',context,request=request)
		return JsonResponse({'data':html})

	context['search_placeholder'] = "Search Music"
	query =request.GET.get('q')

	if query:
		context['title'] = query
		track = track.filter(Q(genre__icontains=query)|
			                 Q(title__icontains=query)).distinct().order_by('-updated_at')

	page = request.GET.get('page', 1)
	paginator = Paginator(track,12)

	try:
		track = paginator.page(page)
	except PageNotAnInteger:
		tracks = paginator.page(1)
	except EmptyPage:
		track = paginator.page(paginator.num_pages)

	context['track'] = track

def paginator_for_album(track,request,context):
	context['search_placeholder'] = "Search Album"
	query =request.GET.get('q')

	if query:
		context['title'] = query
		track = track.filter(Q(artist__icontains=query)|
			                 Q(title__icontains=query)).distinct().order_by('-updated_at')

	page = request.GET.get('page', 1)
	paginator = Paginator(track,12)

	try:
		track = paginator.page(page)
	except PageNotAnInteger:
		tracks = paginator.page(1)
	except EmptyPage:
		track = paginator.page(paginator.num_pages)

	if request.is_ajax() and request.GET.get('pops'):#Popups/needed items ajax
		popups_advert(request,context)
		html = render_to_string('index/selected_place_order.html',context,request=request)
		return JsonResponse({'data':html})

	context['album'] = track

@login_required(login_url="account:google_login")	
def user_music_list(request,args_M = None):

	context = {}
	
	context['music_image'] = "show_music_bacground_image"
	cart_count(request.user,context)
	vendor_account(context,request)

	try:#for editing button
	    Paid_bill   = BillPlan.objects.get(user=request.user)
	    context['user_bill'] = Paid_bill

	except BillPlan.DoesNotExist:
		pass


	if request.session.has_key('added_sucessfuly_msg'):
		context['added_sucessfuly_msg'] = request.session['added_sucessfuly_msg']
		del request.session['added_sucessfuly_msg']

	Vendor = vendor.objects.get(user=request.user)

	if args_M == "Your album list":
		context['for_album'] = "display album list"
		context['title'] = "Your album list"
		
		album = Album.objects.filter(vendor=Vendor).order_by('-updated_at')
		paginator_for_album(album,request,context)

	if args_M == "Non aproved album":
		context['for_album'] = "display album list"
		context['for_non_album'] = "?????"#
		context['title'] = "Non approved album"
		
		album = Album.admin_album_objects.filter(vendor=Vendor).order_by('-updated_at')
		paginator_for_album(album,request,context)

	elif args_M == "Non proved song":
		context['for_non_music'] = "?????"#
		context['title'] = "Non approved song"

		try:
			track = Music.admin_music_objects.filter(user=request.user)
			paginator_for_track(track,request,context)

		except Album.DoesNotExist:
			pass

	else:
		context['title'] = "Approved song"
		track = Music.objects.filter(user=request.user)
		
		paginator_for_track(track,request,context)

	if request.is_ajax() and request.GET.get('pops'):#Popups/needed items ajax
		popups_advert(request,context)
		html = render_to_string('index/selected_place_order.html',context,request=request)
		return JsonResponse({'data':html})

	elif request.is_ajax():# Deleting music/track

		data = request.GET.get('data')
		track_to_delete = Music.objects.get(id=data)
		track_to_delete.delete()
		context['deleted_sucessfuly_msg'] = "Track deleted successfuly"

		context['title'] = "Approved song"
		track = Music.objects.filter(user=request.user)
		context['track'] = track 

		html = render_to_string('music/user_music2.html',context,request=request)
		return JsonResponse({'data':html})

	return render(request,'music/user_music.html',context)

@login_required(login_url="account:google_login")
def add_youtube_feed(request,id=None):

	if request.user.is_superuser:
		context = {}
		context['title'] = "Add youtube video"

		cart_count(request.user,context)
		vendor_account(context,request)

		if request.method == "POST":
			form =youtubefeed_form(request.POST)

			if form.is_valid():
				instance = form.save(commit=False)
				instance.user = request.user
				instance.save()
				request.session['added_sucessfuly_msg'] = "Item added successfuly"
				return redirect('account:dashboard')

		else:
			form =youtubefeed_form()

		context['form'] = form

	else:
		return redirect('index:index')

	return render(request,'music/form.html',context)


def youtube_feed_list(request,CATE=None):

	context = {}

	context['title'] = "Youtube feed"
	context['search_placeholder'] = "Search video"

	cart_count(request.user,context)
	vendor_account(context,request)


	if CATE:
		context['title'] = CATE
		youtubefeed = Youtubefeed.objects.filter(category=CATE).order_by('-updated_at')
	else:
		context['title'] = "Youtube feed"
		youtubefeed = Youtubefeed.objects.all().order_by('-updated_at')

	query =request.GET.get('q')

	if query:
		context['title'] = query
		youtubefeed = youtubefeed.filter(Q(category__icontains=query)|
			                             Q(title__icontains=query)).distinct().order_by('-updated_at')

	page = request.GET.get('page', 1)
	paginator = Paginator(youtubefeed,12)

	try:
		youtubefeed = paginator.page(page)

	except PageNotAnInteger:
		youtubefeed = paginator.page(1)

	except EmptyPage:
		youtubefeed = paginator.page(paginator.num_pages)

	context['youtubefeed'] = youtubefeed
	context['popular'] = product.objects.all().order_by('-view')


	if request.is_ajax() and request.GET.get('pops'):#Popups/needed items ajax
		popups_advert(request,context)
		html = render_to_string('index/selected_place_order.html',context,request=request)
		return JsonResponse({'data':html})

	return render(request,'music/youtube_feed_list.html',context)