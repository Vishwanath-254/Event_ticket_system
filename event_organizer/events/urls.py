from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('login/', views.login_user, name="login"),

    path('events/', views.event_list, name="event_list"),

    path('register/<int:event_id>/', views.register_event, name="register_event"),
    path('cancel-registration/<int:event_id>/', views.cancel_registration, name="cancel_registration"),

    path('my-events/', views.my_events, name="my_events"),

    path('organizer-dashboard/', views.organizer_dashboard, name="organizer_dashboard"),

    path('logout/', views.logout_user, name="logout"),

    path('create-event/',views.create_event,name="create_event"),
    path('edit-event/<int:event_id>/', views.edit_event, name="edit_event"),
    path('delete-event/<int:event_id>/', views.delete_event, name="delete_event"),
    path('event/<int:event_id>/attendees/', views.event_attendees, name='event_attendees'),

    path('event/<int:event_id>/', views.event_detail, name='event_detail'),

    path('dashboard/student/',views.student_dashboard,name="student_dashboard"),

    path('profile/',views.profile_view,name="profile"),

    path('signup/',views.signup_user,name="signup"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
