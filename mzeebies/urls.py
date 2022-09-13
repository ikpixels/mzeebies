from django.contrib import admin
from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django .conf.urls. static import static
from django .conf import settings
from django.contrib.auth import views as auth_views
from django.views.static import serve
from django.conf.urls import handler404, handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('index.urls')),
    path('help/',include('help.urls')),
    path('blog/',include('blog.urls')),
    path('products/',include('products.urls')),
    path('music/',include('music.urls')),
    path('account/',include('account.urls')),
    path('cart/',include('cart.urls')),
    path('vendor/',include('vendor.urls')),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    #path("stripe/", include("djstripe.urls", namespace="djstripe")),
    path('paypal/', include('paypal.standard.ipn.urls')),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='account/password_reset.html',
             subject_template_name='account/password_reset_subject.txt',
             email_template_name='account/password_reset_email.html',
             # success_url='/login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='account/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='account/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='account/password_reset_complete.html'
         ),
         name='password_reset_complete'),

]

#handler404 = views.error_404
#handler500 = views.error_500


urlpatterns+=staticfiles_urlpatterns()

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

