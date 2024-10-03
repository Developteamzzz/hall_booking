from django.urls import path
from .import views
urlpatterns = [
    path('',views.index, name='index'),
    path('index',views.index, name='index'),
    path('login',views.adminlogin, name='adminlogin'),
    path('register',views.adminregister, name='adminregister'),
    path('hall',views.hallmanage, name='hallmanage'),
    path('viewhall',views.viewhall, name='viewhall'),
    path('delete_hall/<int:id>/',views.delete_hall, name='delete_hall'),
    path('updatehall/<int:id>/',views.updatehall, name='updatehall'),
    path('feature',views.featuremanage, name='featuremanage'),
    path('inoperability',views.hallinoperabilitymanage, name='hallinoperabilitymanage'),
    path('update_inoperability/<int:id>/',views.update_inoperability, name='update_inoperability'),
    path('delete_inoperability/<int:id>/',views.delete_inoperability, name='delete_inoperability'),
    path('payment',views.paymentmanage, name='paymentmanage'),
    path('update_feature/<int:id>/',views.update_feature, name='update_feature'),
    path('delete_feature/<int:id>/',views.delete_feature, name='delete_feature'),
    path('calendar/', views.calendarview, name='calendarview'),
    path('cal', views.cal, name='cal'),
    path('get_bookings/<int:hall_id>/', views.get_bookings, name='get_bookings'),
    path('booked', views.booked, name='booked'),
    path('logout',views.logout, name='logout'),
]

