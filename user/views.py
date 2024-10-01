from django.shortcuts import render, redirect, get_object_or_404
from django.http import *
from . models import *
from django.urls import reverse
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
from datetime import datetime, timedelta
from django.core.files.storage import FileSystemStorage

randomotp = 123456


def index(request):
    
    halls_with_images = []
    
    halls = Hall.objects.all()
    print(f"Number of halls fetched: {halls.count()}")
    for hall in halls:
        # Get the first image for the hall, if it exists
        first_image = HallImage.objects.filter(hall=hall).first()
        image_url = first_image.image.url if first_image else None
        halls_with_images.append({
            'hall': hall,
            'image': image_url  # Get the URL if an image exists
        })
        print(f"Hall: {hall.name}, Image URL: {image_url}")
        
    context = {
    'halls_with_images': halls_with_images,
    }
    
    print(context)

    return render(request, 'index.html', context)


def new(request,hall_id=None):
    print(hall_id)
    if hall_id:
        return render(request, 'new_booking.html', {'hall_id':hall_id})
    else:
        return render(request, 'new_booking.html')

   

def about(request):
    return render(request, 'about.html')


def home(request):
    return render(request, 'hallbooking_app/home.html')


def calendar_view(request):
    hall_id=request.GET.get('hall_id')
    print(hall_id)
    return render(request, 'calendar.html', {'hall_id' : hall_id})


def book_hall(request,hall_id=None):
    if request.method == 'POST':
        # Check if OTP is already verified (in the session)
        if not request.session.get('otp_verified', False):
            return JsonResponse({'success': False, 'message': 'OTP verification required'}, status=400)
        
        # Now proceed with the rest of the form data
        name = request.POST.get('name')
        number = request.POST.get('number')
        address = request.POST.get('address')
        startDate = request.POST.get('start_date')
        event_type = request.POST.get('event_type')
        event_details = request.POST.get('specify') if event_type == 'others' else None
        event_description = request.POST.get('event_description')
        timeslot = request.POST.get('timeslot')
        
        if(hall_id==None):
            hall_id=request.POST.get('hall_id)') 
        print(hall_id)
        selected_hall = Hall.objects.get(id=hall_id)
        print(selected_hall)
        evening_before = request.POST.get('eveningBefore')
        features = request.POST.getlist('features')

        # Retrieve the email from the session
        email = request.session.get('email')

        # Create the user contact details
        user_contact = User.objects.create(
            name=name, number=number, email=email, address=address
        )
        
        # Create the booking
        booking = Booking.objects.create(
            
            date=startDate,
            user=user_contact,
            program=event_type if event_type != 'others' else event_details,
            description=event_description,
            approval_status=0,
            ac=1,
            timeslot=timeslot,
            evening_before=evening_before,
            features=', '.join(features),
            hall=selected_hall,
            
        )

        # Handle "full day" booking case
        if timeslot == "full":
            d1 = startDate
            date = datetime.strptime(d1, "%Y-%m-%d")
            day_before = (date - timedelta(days=1)).date()
            
            booking2 = Booking.objects.create(
                date=day_before,
                user=user_contact,
                program=event_type if event_type != 'others' else event_details,
                description=event_description,
                approval_status=0,
                ac=1,
                timeslot="evening",
                evening_before=evening_before,
                features=', '.join(features),
                hall=selected_hall,  # Assuming the same hall is selected
            )

        return JsonResponse({'success': True, 'message': 'Hall booked successfully'})

    else:
        start_date = request.GET.get('start_date', None)
        timeslot = request.GET.get('timeslot', None)
        available_halls = []

        if start_date and timeslot:
            booked_halls = Booking.objects.filter(date=start_date, timeslot=timeslot).values_list('hall_id', flat=True)
            available_halls = Hall.objects.exclude(id__in=booked_halls)
            print(available_halls)
            print(booked_halls)

        return render(request, 'new_booking.html', {
            'available_halls': available_halls,
        })

# def book_hall(request):
#     if request.method == 'POST':
#         # Check if the OTP is already verified
#         if not request.session.get('otp_verified', False):  # Check if OTP is verified in session
#             return JsonResponse({'success': False, 'message': 'OTP verification required'}, status=400)
        
#         name = request.POST.get('name')
#         number = request.POST.get('number')
#         address = request.POST.get('address')
#         startDate = request.POST.get('start_date')
#         event_type = request.POST.get('event_type')
#         event_details = request.POST.get('specify') if event_type == 'others' else None
#         event_description = request.POST.get('event_description')
#         timeslot = request.POST.get('timeslot')
#         hall_id = request.POST.get('hall')
#         selected_hall = Hall.objects.get(id=hall_id)

#         evening_before = request.POST.get('eveningBefore')
#         features = request.POST.getlist('features')
#         print(f"Evening Before: {evening_before}")
#         print(f"Features: {features}")
        
#         # Create the user contact details
#         user_contact = User.objects.create(
#             name=name, number=number, email=request.POST.get('email'), address=address
#         )
        
#         # Create the booking
#         booking = Booking.objects.create(
#             date=startDate,
#             user=user_contact,
#             program=event_type if event_type != 'others' else event_details,
#             description=event_description,
#             approval_status=0,
#             ac=1,
#             timeslot=timeslot,
#             evening_before=evening_before,
#             features=', '.join(features),
#             hall=selected_hall,
#         )

#         # Handle the "full day" scenario with additional booking for evening before
#         if timeslot == "full":
#             d1 = startDate
#             date = datetime.strptime(d1, "%Y-%m-%d")
#             day_before = (date - timedelta(days=1)).date()
            
#             booking2 = Booking.objects.create(
#                 date=day_before,
#                 user=user_contact,
#                 program=event_type if event_type != 'others' else event_details,
#                 description=event_description,
#                 approval_status=0,
#                 ac=1,
#                 timeslot="evening",
#                 evening_before=evening_before,
#                 features=', '.join(features),
#                 hall=selected_hall,  # Assuming same hall is selected
#             )

#         return JsonResponse({'success': True, 'message': 'Hall booked successfully'})

#     else:
#         start_date = request.GET.get('start_date', None)
#         timeslot = request.GET.get('timeslot', None)
#         available_halls = []

#         if start_date and timeslot:
#             booked_halls = Booking.objects.filter(date=start_date, timeslot=timeslot).values_list('hall_id', flat=True)
#             available_halls = Hall.objects.exclude(id__in=booked_halls)
#             print(available_halls)
#             print(booked_halls)

#         return render(request, 'new_booking.html', {
#             'available_halls': available_halls,
#         })

# def fetch_bookings(request):
#     if request.method == 'GET':
#         bookings = Booking.objects.all().values('date', 'timeslot')  # Fetch booking date and timeslot
#         booking_list = list(bookings)
#         return JsonResponse(booking_list, safe=False)

# def fetch_bookings(request):
#     if request.method == 'GET':
#         hall_id = request.GET.get('hall_id')
#         if hall_id:
#             bookings = Booking.objects.filter(hall_id=hall_id).values('date', 'timeslot')
#         else:
#             bookings = []
#         booking_list = list(bookings)
#         return JsonResponse(booking_list, safe=False)


def fetch_bookings(request, hall_id):
    bookings = Booking.objects.filter(hall_id=hall_id).values('date', 'timeslot')
    return JsonResponse(list(bookings), safe=False)


def generate_otp():
    """Generate a 6-digit OTP"""
    return random.randint(100000, 999999)


def check_availability(request):
    date = request.GET.get('date')
    timeslot = request.GET.get('timeslot')
    hall_id = request.GET.get('hall_id')
    
    is_available = not Booking.objects.filter(hall_id=hall_id, date=date, timeslot=timeslot).exists()
    return JsonResponse({'available': is_available})

# def send_otp(request):
#     if request.method == 'POST':
#         request.session['test'] = 'test_value'
#         print("Session before setting OTP:", request.session.items())

#         data = json.loads(request.body)
#         email = data.get('email')
#         print("Email received:", email)

#         otp = generate_otp()
#         request.session['otp'] = str(otp)
#         request.session['email'] = email
#         request.session.modified = True  # Mark session as modified
        
#         print("Stored OTP in session:", request.session.get('otp'))
#         print("Session data after setting OTP:", request.session.items())

#         userotp = User_OTP.objects.create(
#                 otp=otp, is_verified=False, user=user_contact,
#         )
#         # Attempt to send OTP via email
#         try:
#             send_mail(
#                 'Your OTP for Hall Booking',
#                 f'Your OTP is {otp}. It is valid for 10 minutes.',
#                 'no-reply@hallbooking.com',
#                 [email],
#                 fail_silently=False,
#             )
#         except Exception as e:
#             print("Error sending email:", e)
#             return JsonResponse({'success': False, 'message': 'Failed to send OTP email'}, status=500)
        
#         return JsonResponse({'success': True, 'message': 'OTP sent successfully'})

#     return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

# def verify_otp(request):
#     if request.method == 'POST':
#         request.session['test'] = 'test_value'  # Just for testing
#         print("Session data in verify_otp:", request.session.items())
#         print("Session ID in verify_otp:", request.session.session_key)

#         data = json.loads(request.body)  # Load the JSON data from the request body
#         entered_otp = data.get('otp')  # Get the OTP from the JSON data
#         session_otp = request.session.get('otp')
#         print("Entered OTP:", entered_otp)
#         print("Stored session OTP:", session_otp)

#         if entered_otp == session_otp:
#             print("OTP verified successfully.")
#             return JsonResponse({'success': True, 'message': 'OTP verified successfully'})
#         else:
#             print("OTP verification failed.")
#             return JsonResponse({'success': False, 'message': 'OTP is incorrect'})

#     return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


def send_otp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        
        # Generate OTP
        otp = generate_otp()  # Make sure this function is implemented
        
        # Store OTP and email in session
        request.session['otp'] = otp
        request.session['email'] = email
        
        # You can print the OTP for testing purposes
        print(f"Generated OTP: {otp}")
        
        return JsonResponse({'success': True, 'message': 'OTP sent successfully'})
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


def verify_otp(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        entered_otp = data.get('otp')
        
        # Retrieve OTP and email from session
        session_otp = str(request.session.get('otp'))
        email = request.session.get('email')
        
        # print("session ",session_otp)
        # print("entered ",entered_otp)
        
        if entered_otp == session_otp:
            # Mark OTP as verified in the session
            request.session['otp_verified'] = True
            return JsonResponse({'success': True, 'message': 'OTP verified successfully'})
        else:
            return JsonResponse({'success': False, 'message': [entered_otp, session_otp] })
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


def test_session(request):
    if request.method == 'POST':
        request.session['test_key'] = 'test_value'
        return JsonResponse({'success': True, 'test_key': request.session['test_key']})
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


def check_session(request):
    otp = request.session.get('otp', 'No OTP found')
    email = request.session.get('email', 'No email found')
    return JsonResponse({'otp': otp, 'email': email})


# View to display the add features form and handle submission
def add_features(request):
    if request.method == "POST":
        hall_id = request.POST.get('hall_id')
        feature_id = request.POST.get('feature_id')
        
        # Create a new HallFeature entry
        HallFeature.objects.create(hall_id=hall_id, feature_id=feature_id)
        
        return redirect('add_features')  # Redirect to the same page after submission

    # Pass the list of halls and features to the template
    halls = Hall.objects.all()
    features = Feature.objects.all()
    
    return render(request, 'add_features.html', {'halls': halls, 'features': features})


# View to display the add images form and handle submission
def add_images(request):
    if request.method == "POST" and request.FILES:
        hall_id = request.POST.get('hall_id')
        images = request.FILES.getlist('image')  # Get multiple images

        # Save each image
        for image in images:
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            HallImage.objects.create(hall_id=hall_id, image=filename)

        return redirect('add_images')  # Redirect to the same page after submission

    # Pass the list of halls to the template
    halls = Hall.objects.all()
    
    return render(request, 'add_images.html', {'halls': halls})


def hall_detail(request, hall_id):
    # Fetch the hall by its ID
    hall = get_object_or_404(Hall, id=hall_id)
    
    # Get all images related to the hall
    images = HallImage.objects.filter(hall=hall)
    
    # Get all features related to the hall (via HallFeature model)
    hall_features = HallFeature.objects.filter(hall=hall)
    features = [hall_feature.feature for hall_feature in hall_features]  # Extract feature objects
    
    context = {
        'hall': hall,
        'images': images,
        'features': features,
    }
    
    return render(request, 'hall_detail.html', context)
