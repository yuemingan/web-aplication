from django.urls import path
from socialnetwork import views

urlpatterns = [
    path('', views.global_action, name='home'),
    path('login', views.login_action, name='login'),
    path('register', views.register_action, name='register'),
    path('logout', views.logout_action, name='logout'),
    path('global', views.global_action, name='global'),
    path('follower', views.follower_action, name='follower'),
    path('myProfile', views.myProfile_action, name='myProfile'),
    path('otherProfile', views.otherProfile_action, name='otherProfile'),
]
