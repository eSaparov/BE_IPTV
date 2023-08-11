from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('video/list', VideosListView.as_view(), name='video_list'),
    path('video/<int:pk>', VideoDetailView.as_view(), name='video_detail'),
    path('login', LoginInterfaceView.as_view(), name='login'),
    path('logout', LogoutInterfaceView.as_view(), name='logout'),

re_path(r'^search_video/', search_video, name="search_video"),
]