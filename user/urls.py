
from django.urls import path
from . import views
urlpatterns = [
    
    path('', views.index, name="index"),
    path('new/', views.new , name="new"),
    path('about/', views.about , name="about"),
    path('generate_otp/', views.generate_otp , name="generate_otp"),
    path('verify_otp/', views.verify_otp , name="verify_otp"),
    path('home/', views.home, name='home'),
    
    # path('list_halls/', views.list_halls, name='list_halls'),
    # path('check_availability/', views.check_availability, name='check_availability'),
    path('book_hall/', views.book_hall, name='book_hall'),
    # path('add_hall/', views.add_hall, name='add_hall'),
    # path('booking_confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('send-otp/', views.send_otp, name='send_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('calendar/', views.calendar_view, name='calendar'),  # URL to view the calendar
    path('fetch-bookings/', views.fetch_bookings, name='fetch_bookings')
    
    #path('step/', views.step , name="step"),
    #path('book/', views.book , name="book"),
    
    # path('otp/', views.otp , name="otp"),
    # path('verify/', views.verify , name="verify"),

    

]
