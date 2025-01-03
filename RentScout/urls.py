from django.urls import path
from .views import (get_room_data, get_room_images, get_rooms,
                    del_room_photo_view, upload_room_photo_view, building_edit_view,
                    get_policies, save_policy_view, del_policy_view, update_policy_view,
                    request_amenity_status, create_amenity_view, update_amenity_view,
                    update_room, create_bookmark, get_bookmark_status, remove_bookmark,
                    get_buildings_bypage, create_building_report, get_all_reports,
                    delete_building_view, delete_building_report, get_verification_status_view,
                    create_verification_view, delete_verification, get_verification_requests,
                    deny_verification, accept_verification, create_room_view, get_bookmark_all,
                    send_payment, generate_email_data, generate_otp, get_mailjs_keys,
                    create_reservation, get_reservation_instance, delete_reservation,
                    get_reservations_pending, accept_reservation, notify_boarder,
                    upload_certificate_view, get_certificate_byid, 
                    get_certificates_view, decline_reservation,
                    delete_reservation_byid, get_messages, request_userid, request_building_userid,
                    create_message, get_inbox, filter_payment, accept_payment, decline_payment,
                    hide_payment, 
                    
                    )
from . import views
from django.conf import settings
from django.conf.urls.static import static
    
urlpatterns = [
    path('', views.home, name="home"),
    path('signup/', views.scoutuser_signup, name='signup'),
    path('signin/', views.scoutuser_login, name="signin"),
    path('logout/', views.scoutuser_logout, name='logout'),
    path('signup/get_otp/', generate_otp.as_view()),
    path('signup/get_keys/', get_mailjs_keys.as_view()),
    # DASHBOARD (HOME PAGE)
    path('home_page/request/buildings/', get_buildings_bypage.as_view()),

    # BUILDINGS
    # path('create_building/', views.create_building, name='new_building'),
    path('edit_building/create_building/', views.create_building_edit_page, name='add_building'),
    path('building_info/<int:pk>/', views.building_info, name = 'building_info'),
    path('building/update/<str:pk>/', views.update_building, name='update_building'),
    path('building/update_view/', building_edit_view.as_view()),
    path('building/edit/', views.building_edit, name='edit_building'),
    path('building/delete_view/', delete_building_view.as_view()),
    path('building/request/verification_status/', get_verification_status_view.as_view()),
    # path()

    # RESERVATIONS
    path('reservations/', views.reservation_page, name = 'reservations'),
    path('reservations/send_notification/', generate_email_data.as_view()),
    path('reservations/create_reservation/', create_reservation.as_view()),
    path('reservations/get/reservation_status/', get_reservation_instance.as_view()),
    path('reservations/delete/', delete_reservation.as_view()),
    path('reservations/get/pending/reservations/', get_reservations_pending.as_view()),
    path('reservations/accept/', accept_reservation.as_view()),
    path('reservations/get/mailjs_keys/', notify_boarder.as_view()),
    path('reservations/decline/', decline_reservation.as_view()),
    path('reservations/delete_byid/', delete_reservation_byid.as_view()),

    # FEEDBACK
    path('building/feedback/', views.create_feedback, name='newfeedback'),
    path('buildling/feedback/update/<str:pk>/', views.update_feedback, name='update_feedback'),

    # ROOMS
    path('room_create/<int:buildingID>', views.room_create, name='room_create'),
    path('room/create_view/', create_room_view.as_view()),
    path('room/request/', get_room_data.as_view(), name='room_update'),
    path('room/get_rooms/', get_rooms.as_view(), name='get_rooms'),
    path('room_update/save/', views.room_update, name='room_save'),
    path('room_update_view/', update_room.as_view()),

    # ROOMPHOTOS
    path('room_photo/upload/', views.room_photo_upload, name='room_photo_upload'),
    path('room_photo/upload/as_view/', upload_room_photo_view.as_view(), name='room_photo_upload_view'),
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
    path('building/amenity_request/', request_amenity_status.as_view()),
    path('building/amenity/update/', update_amenity_view.as_view()),


    # USERPROFILE
    path('user/user_profile/', views.user_profile, name='user_profile'),
    path('user/user_profile/update/', views.update_user_profile, name='update_user_profile'),
    path('user/user_profile_admin_access/<int:userid>/', views.user_profile_admin_access, name='user_profile_admin_access'),
    
    # MAP 
    path('building/map/', views.go_map, name='map'),
    
    # REPORTS
    path('building/reports/view/', views.all_reports, name='reports_page'),
    path('building/create_report/', create_building_report.as_view()),
    path('buildings/report/get_all/', get_all_reports.as_view()),
    path('building/reports/delete/', delete_building_report.as_view()),

    # VERIFICATION
    path('building/verification/', views.all_verification, name = 'verification_page'),
    path('building/create_verification/', create_verification_view.as_view()),
    path('building/remove_verification/', delete_verification.as_view()),
    path('building/request/verification_requests/', get_verification_requests.as_view()),
    path('building/deny_verification/', deny_verification.as_view()),
    path('building/accept_verification/', accept_verification.as_view()),
    
    # BOOKMARKS
    path('user/bookmark/', views.bookmark_page, name='bookmark_page'),
    path('user/bookmark/request/', get_bookmark_all.as_view()),
    path('user/bookmark/add/', create_bookmark.as_view(), name='add_bookmark'),
    path('user/bookmark/building/page/', get_bookmark_status.as_view()),
    path('user/bookmark/delete/', remove_bookmark.as_view()),

    # CERTIFICATES
    path('certificate/upload/', upload_certificate_view.as_view()),
    path('certificates/get/', get_certificates_view.as_view()),
    path('certificate/get_byid/', get_certificate_byid.as_view()),
    
    # MESSAGES
    path('inbox/get_inbox/', get_inbox.as_view()),
    path('messages/building/get_owner_id/', request_building_userid.as_view()),
    path('messages/get_user/', request_userid.as_view()),
    path('messages/request/', get_messages.as_view()),
    path('messages/send_message/', create_message.as_view()),

    #PAYMENTS
    path('payment/send/', send_payment.as_view()),
    path('payment/filter/', filter_payment.as_view()),
    path('payment/accept/', accept_payment.as_view()),
    path('payment/decline/', decline_payment.as_view()),
    path('payment/hide/', hide_payment.as_view()),
    # SCRAPPERS
    path('scrapper/building/', views.building_file_scrapper, name='building_scrapper'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)