from django.urls import path
from . import views
    
urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.scoutuser_signup, name='signup'),
    path('signin/', views.scoutuser_login, name="signin"),
    path('logout/', views.scoutuser_logout, name='logout'),
]