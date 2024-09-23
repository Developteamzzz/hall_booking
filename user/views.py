from django.shortcuts import render, redirect, get_object_or_404
from django.http import *
from . models import *
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.core import serializers
import random
from django.core.mail import send_mail
from django.conf import settings
from django.utils import *
from django.contrib import messages
from django.utils import timezone
import logging
import json
from django.core.cache import cache


randomotp = 123456


def index(request):
    return render(request, 'index.html')


def new(request):
    return render(request, 'new_booking.html')


def about(request):
    return render(request, 'about.html')


def home(request):
    return render(request, 'hallbooking_app/home.html')


def book_hall(request):
    if request.method == 'POST':
        # If the user has entered an OTP
        request.session.flush()
        if 'otp' in request.POST.get('otp'):
            otp_response = verify_otp(request)
            if otp_response.get('success'):
                # OTP is verified, proceed with the booking
                name = request.POST.get('name')
                number = request.POST.get('number')
                address = request.POST.get('address')
                hall_id = request.POST.get('hall')
                startDate = request.POST.get('start_date')
                event_type = request.POST.get('event_type')
                event_details = request.POST.get('specify') if event_type == 'others' else None
                event_description = request.POST.get('event_description')
                timeslot = request.POST.get('timeslot')
                # Save user contact
                user_contact = User.objects.create(
                    name=name, number=number, email=request.session['email'], address=address
                )

                # Create the booking
                booking = Booking.objects.create(
                    
                    date=startDate,
                    hall_id=1,
                    user_id=user_contact,
                    program=event_type if event_type != 'others' else event_details,
                    description=event_description,
                    approval_status=0,
                    ac=1,
                    timeslot=timeslot,
                )

                return redirect('index')

            else:
                messages.error(request, 'Invalid OTP. Please try again.')

        else:
            # First step: user enters email, generate OTP and send
            send_otp(request)
            messages.success(request, 'OTP has been sent to your email.')

    return render(request, 'new_booking.html')


def fetch_bookings(request):
    bookings = Booking.objects.all().values('date')  # Adjust based on your model
    response_data = [
        {
            'date': booking['date'],
            'title': 'Your Event Title'  # You can customize this title as needed
        } 
        for booking in bookings
    ]
    return JsonResponse(response_data, safe=False)


def calendar_view(request):
    return render(request, 'calendar.html')

# def verify_otp(request):
#     if request.method == 'POST':
#         otp = request.POST.get('otp')
#         email = request.session.get('email')

#         try:
#             booking = User.objects.get(email=email)
#             if booking.otp == otp:
#                 booking.is_verified = True
#                 booking.otp = ''
#                 booking.save()
#                 return JsonResponse({'status': 'success', 'message': 'OTP verified.'})
#             else:
#                 return JsonResponse({'status': 'error', 'message': 'Invalid OTP.'})
#         except User.DoesNotExist:
#             return JsonResponse({'status': 'error', 'message': 'Email not found.'})


def generate_otp():
    """Generate a 6-digit OTP"""
    return random.randint(100000, 999999)


def send_otp(request):
    if request.method == 'POST':
        request.session['test'] = 'test_value'  # Create a test session variable
        print("Test session data:", request.session.items())
        data = json.loads(request.body)
        email = data.get('email')
        # email = request.POST.get('email')
        print(email)
        otp = generate_otp()
        randomotp = otp
        print("global = ", randomotp)
        # Save OTP and email in session
        request.session['otp'] = str(otp)
        request.session['temp_otp'] = otp

        
        print(f"Stored OTP in session: {request.session['otp']}")
        print(request.session['otp'])
        request.session['email'] = email
        
        print("Session data before setting OTP:", request.session.items())
        request.session['otp'] = otp
        print("Session data after setting OTP:", request.session.items())
        print("Session ID in send_otp:", request.session.session_key)

        
        print("Current session cache:", cache.get('session_key'))

        # Send OTP via email (assuming you have email settings configured)
        send_mail(
            'Your OTP for Hall Booking',
            f'Your OTP is {otp}. It is valid for 10 minutes.',
            'no-reply@hallbooking.com',
            [email],
            fail_silently=False,
        )
        print(f"Sending OTP {otp} to {email}")
        print(f"Session data after sending OTP: {request.session.items()}")
        return JsonResponse({'success': True, 'message': 'OTP sent successfully'})
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


def verify_otp(request):
    
    if request.method == 'POST':
        request.session['test'] = 'test_value'  # Create a test session variable
        print("Test session data:", request.session.items())
        print("Session data in verify_otp:", request.session.items())
        print("Session ID in verify_otp:", request.session.session_key)
        
        data = json.loads(request.body)  # Load the JSON data from the request body
        entered_otp = data.get('otp')  # Get the OTP from the JSON data
        session_otp = str(request.session.get('otp'))
        print(entered_otp)
        print(session_otp)
        print(randomotp)
        if entered_otp == session_otp:
            
            print("ok")
            return JsonResponse({'success': True, 'message': 'OTP verified successfully'})

        else:
            print("no")
            return JsonResponse({'success': False, 'message': 'OTP is incorrect'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


def test_session(request):
    if request.method == 'POST':
        request.session['test'] = 'test_value'
        return JsonResponse({'success': True})

    value = request.session.get('test', 'not set')
    return JsonResponse({'session_value': value})


# def list_halls(request):
#     halls = Hall.objects.all()  # Fetch all halls from the database
#     return render(request, 'hallbooking_app/list_halls.html', {'halls': halls})

# def booking_confirmation(request, booking_id):
#     # Fetch the booking details using the booking_id
#     booking = get_object_or_404(Booking, id=booking_id)
#     user = booking.user_contact
#     print(user)
    
#     # Pass the booking details to the template
#     return render(request, 'hallbooking_app/booking_confirmation.html', {'booking': booking,'user': user,})

# def generate_otp(request):
    
#     if request.method == 'POST':
#         email = request.POST.get('email')

#         booking, created = User.objects.get_or_create(email=email, number='584',)

#         # Generate and send OTP
#         otp = generate_otp2()
#         booking.otp = otp
#         booking.save()

#         send_otp_email(email, otp)

#         request.session['email'] = email  # Save email in session for next step

#         return JsonResponse({'status': 'success', 'message': 'OTP sent successfully.'})

# def otp(request):
#     print("keruo ?")
#     if request.method == 'POST':
#         print("keri !")
#         email = request.POST.get('email')
#         print(email)
#         otp = generate_otp()
#         print(otp)
#         send_otp_email(email, otp)
#     return render(request, 'index.html')

# def book(request):
#     user = User.objects.all()
#     book = Booking.objects.all()
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         date = request.POST.get('start_date')
#         timeslot = request.POST.get('start_time')
#         description = request.POST.get('description')
#         program = request.POST.get('program')
#         contact = request.POST.get('contact')
#         ac = request.POST.get('ac')
#         email = request.POST.get('email')
#         address = request.POST.get('address')
#         event = User.objects.create(
# 			name=name,
#             contact=contact,
#             email=email,
#             address=address,
# 		)
#         booked = Booking.objects.create(
# 			date=date,
#             program=program,
#             timeslot=timeslot,
# 			description=description,
# 			approval_status=False,
#             ac = ac,
# 		)
#     else:
#         return render(request, 'booking_app/create_event.html', {'event': user})
    
#     return render(request, 'booking.html')

# def step(request):
#     return render(request, 'step_booking.html')

# def create_event(request):
    
#     categories = User.objects.all()
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         start_date = request.POST.get('start_date')
#         start_time = request.POST.get('start_time')
#         description = request.POST.get('description')
#         organizer = request.POST.get('organizer')
#         contact = request.POST.get('contact')
        
#         User = User.objects.create(
# 			name=name,
#             contact=contact,
# 			start_date=start_date,
#             start_time=start_time,
# 			description=description,
# 			organizer=organizer,
# 		)
        
#         return redirect('category_events')
#     else:
#         return render(request, 'booking_app/create_event.html', {'event': categories})

# def register(request):
#     if request.method == 'POST':
#         # username = request.POST['username']
#         # password = request.POST['password']
#         email = request.POST['email']
#         # contact = request.POST.get('contact')
#         # address = request.POST.get('address')
#         #user = User.objects.create(username=username, password=password, email=email, contact = contact, address = address, )
        
#         # Generate OTP and send it via email
#         otp = generate_otp()
#         # user.otp = otp
#         # user.save()
#         send_otp_email(email, otp)
#         return redirect('verify')  # Redirect to OTP verification page
#     return render(request, 'new_booking.html')

# def verify(request):
#     if request.method == 'POST':
#         rotp = request.POST.get('otp')
#         if rotp == otp:
#             return JsonResponse({'status': 'success', 'message': 'OTP verified successfully.'})
#         else:
#             return JsonResponse({'status': 'error', 'message': 'Invalid OTP. Please try again.'})

#     return JsonResponse({'status': 'error', 'message': 'Invalid request.'})

# def verify_email(request, user_id):
#     user = User.objects.get(id=user_id)

#     if request.method == 'POST':
#         entered_otp = request.POST['otp']
        
#         if entered_otp == user.otp:
#             user.is_verified = True
#             user.otp = ''  # Clear OTP
#             user.save()
#             return redirect('login')  # Redirect to login after verification
        
#         else:
#             error = 'Invalid OTP. Please try again.'
#             return render(request, 'verify_email.html', {'error': error})

#     return render(request, 'verify_email.html', {'user_id': user_id})

# def booking_confirmation(request, booking_id):
#     # Fetch the booking details using the booking_id
#     booking = get_object_or_404(Booking, id=booking_id)
#     user = booking.user_contact
#     print(user)
    
#     # Pass the booking details to the template
#     return render(request, 'hallbooking_app/booking_confirmation.html', {'booking': booking,'user': user,})

# def send_otp_email(email, otp):
    
#     subject = 'Your OTP for registration'
#     message = f'Your One-Time Password (OTP) is {otp}. Please enter it to verify your email.'
#     from_email = settings.EMAIL_HOST_USER
#     send_mail(subject, message, from_email, [email])

