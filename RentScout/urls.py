from django.urls import path
from .views import (get_room_data, get_room_images, get_rooms,
                    del_room_photo_view, upload_room_photo_view, building_edit_view,
                    get_policies, save_policy_view, del_policy_view, update_policy_view,
                    # request_amenity_status
                    create_amenity_view
                    )
from . import views
from django.conf import settings
from django.conf.urls.static import static
    
urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.scoutuser_signup, name='signup'),
    path('signin/', views.scoutuser_login, name="signin"),
    path('logout/', views.scoutuser_logout, name='logout'),

    # BUILDINGS
    path('create_building/', views.create_building, name='new_building'),
    path('building_info/<int:pk>/', views.building_info, name = 'building_info'),
    path('building/update/<str:pk>/', views.update_building, name='update_building'),
    path('building/update_view/', building_edit_view.as_view()),
    path('building/edit/', views.building_edit, name='edit_building'),

    # FEEDBACK
    path('building/feedback/', views.create_feedback, name='newfeedback'),
    path('buildling/feedback/update/<str:pk>/', views.update_feedback, name='update_feedback'),

    # ROOMS
    path('room_create/<int:buildingID>', views.room_create, name='room_create'),
    path('room_update/', get_room_data.as_view(), name='room_update'),
    path('room/get_rooms/', get_rooms.as_view(), name='get_rooms'),
    path('room_update/save/', views.room_update, name='room_save'),

    # ROOMPHOTOS
    path('room_photo/upload/', views.room_photo_upload, name='room_photo_upload'),
    path('room_photo/upload/as_view', upload_room_photo_view.as_view(), name='room_photo_upload_view'),
    path('room_photo/request/', get_room_images.as_view(), name='get_room_images'),
    path('room_photo/edit/<int:pk>/', views.room_edit_photo, name='edit_photo'),
    path('room_photo/delete/', views.room_delete_photo, name='del_room_photo'),
    path('room_photo/delete/view/', del_room_photo_view.as_view(), name='del_room_photo_view'),

    # POLICIES
    path('building/policies_request/', get_policies.as_view()),
    path('building/policy/add_new/', save_policy_view.as_view()),
    path('building/policy/delete/', del_policy_view.as_view()),
    path('building/policy/update/', update_policy_view.as_view()),

    # AMENITIES
    path('building/amenity/create_new/', create_amenity_view.as_view()),
    # path('building/amenity_request/', request_amenity_status.as_view()),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)