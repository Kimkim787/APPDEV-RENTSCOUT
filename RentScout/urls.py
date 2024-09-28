from django.urls import path
from .views import get_room_data, get_room_images
from . import views
from django.conf import settings
from django.conf.urls.static import static
    
urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.scoutuser_signup, name='signup'),
    path('signin/', views.scoutuser_login, name="signin"),
    path('logout/', views.scoutuser_logout, name='logout'),
    path('create_building/', views.create_building, name='new_building'),
    path('building_info/<int:pk>/', views.building_info, name = 'building_info'),
    path('building/update/<str:pk>/', views.update_building, name='update_building'),

    # ROOMS
    path('room_create/<int:buildingID>', views.room_create, name='room_create'),
    path('room_update/', get_room_data.as_view(), name='room_update'),
    path('room_update/save/', views.room_update, name='room_save'),

    # ROOMPHOTOS
    path('room_photo/upload/', views.room_photo_upload, name='room_photo_upload'),
    path('room_photo/request/', get_room_images.as_view(), name='get_room_images'),
    path('room_photo/edit/<int:pk>/', views.room_edit_photo, name='edit_photo'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)