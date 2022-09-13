from . import views
from django.urls import path

app_name = "help"

urlpatterns = [
    path('help_&_support/',views.help,name="help"),
   ]
