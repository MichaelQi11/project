from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url

urlpatterns = [
	path('', views.LoginView.as_view(), name = 'login'),
	path('logout', views.logout_view, name = 'logout'),
	path('signup',views.signup,name = 'signup'),
	path('main', views.main_page, name = 'main_page'),
	#path('author', views.getUserProfile, name = 'userprofile')
	path('new_post', views.new_post, name = 'new_post'),
	# path('main', views.finish_post, name = 'main_page'),
	path('post_form', views.AddPostView.as_view(), name="post_form"),

	path('like', views.like_view, name="like_post")
]
