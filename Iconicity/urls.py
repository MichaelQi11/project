from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('', views.LoginView.as_view(), name = 'login'),
	path('logout', views.logout_view, name = 'logout'),
	path('signup',views.signup,name = 'signup'),
	path('main', views.main_page, name = 'main_page'),

	# need to fix this part later
	path('friends/like', views.like_view, name="like_post_friend"),
	path('mypost/like', views.like_view, name="like_post_mypost"),
	path('public/like', views.like_view, name="like_post_public"),
	path('following/like', views.like_view, name="like_post_following"),

	path('repost', views.repost, name='repost'),
	path('profile',views.profile,name = "profile"),
	path('mypost', views.mypost, name = 'my_post'),
	path('public',views.mainPagePublic,name = "main_page"),
	path('friends', views.friends, name = 'friends'),
	path('following',views.following,name = "follow"),
	path('post_form', views.AddPostView.as_view(), name="post_form"),
	path('friend_requests', views.friendRequests_received_view, name='friend_requests'),
	path('avail_profiles', views.userProfile_list_view, name='avail_profiles'),


	# APIs
    path(r'posts/', views.Posts().as_view()),
    path(r'posts', views.Posts().as_view()),
	path(r'posts/<str:post_id>/', views.PostById().as_view()),
    path(r'posts/<str:post_id>', views.PostById().as_view()),





] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
