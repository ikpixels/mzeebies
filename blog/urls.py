from . import views
from django.urls import path

app_name = "blog"

urlpatterns = [
    path('blog/',views.blog,name="blog"),
    path('blog/<cate>/',views.blog,name="blog2"),
    path('blog_detail/<slug>/',views.blog_detail,name="blog_detail"),
    path('addblog/',views.AddBlog,name="AddBlog")
]
