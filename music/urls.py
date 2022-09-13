#Author Isaac Kakodwa
from . import views
from django.urls import path

app_name = "music"

urlpatterns = [
    path('music/',views.music,name="music"),
    path('music/<args_1>/',views.music,name="music_1"),
    path('main_music/',views.main_music,name="main_music"),
    path('main_music2/<args>/',views.main_music,name="main_music_2"),
    path('music_2/<other_args>/',views.music,name="music_2"),
    path('user_music_list/',views.user_music_list,name='user_music'),
    path('user_music_list2/<args_M>/',views.user_music_list,name='user_music2'),
    path('album_list/<CATEGORY>/',views.album_list,name="album_list"),
    path('album_list2/<TOP_TEN>/',views.album_list,name="album_top_ten"),
    path('album_list_detail/<slug>/',views.album_list_detail,name="album_list_detail"),
    path('album_list_detail2/<slug_2>/',views.album_list_detail,name="album_list_detail2"),
    path('create_album/',views.create_album,name="create_album"),
    path('add_track',views.add_track,name="add_track"),
    path('edit_track/<int:edit_track_id>/',views.add_track,name="edit_track"),
    path('add_track/<slug>/',views.add_track,name="add_track2"),
    path('music_detail/<slug>/',views.music_detail,name="music_detail"),
    path('add_youtube_feed/',views.add_youtube_feed,name="add_youtube_feed"),
    path('youtube_feed_list/',views.youtube_feed_list,name="youtube_feed_list"),
    path('youtube_feed/<CATE>/',views.youtube_feed_list,name="youtube_feed_CATE")
]
