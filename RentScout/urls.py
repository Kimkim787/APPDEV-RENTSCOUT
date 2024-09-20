from django.urls import path
from . import views
    
urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.scoutuser_signup, name='signup'),
    path('signin/', views.scoutuser_login, name="signin"),
    path('logout/', views.scoutuser_logout, name='logout'),
    path('create_building/', views.create_building, name='new_building'),
    path('building_info/<int:pk>/', views.building_info, name = 'building_info'),
    path('building/update/<str:pk>/', views.update_building, name='update_building'),

    path('room_create/<int:buildingID>/', views.room_create, name='room_create'),
]