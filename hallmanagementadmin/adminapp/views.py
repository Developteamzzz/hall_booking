from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.utils import timezone
import calendar
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
    return render(request,'index.html')

def adminregister(request):
    if request.method == "POST":
        username= request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
         # Check if superadmin checkbox is checked
        superadmin = 1 if request.POST.get('superadmin') else 0
        reg=Adminrecord.objects.create(
            username=username,
            password=password,
            email=email,
            superadmin=superadmin,
            )
    return render(request,'register.html')


def adminlogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Validate the username and password are provided
        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return render(request, 'login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if the user is an admin
            if user:  # Assuming admin users are superusers
                login(request, user)
                messages.success(request, "Login successful!")
                return render(request,'index.html')
            else:
                messages.error(request, 'You do not have permission to access this area.')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

def hallmanage(request):
    if request.method == "POST":
        # Collect hall details from the form
        hallname = request.POST.get('hallname')
        place = request.POST.get('place')
        landmark = request.POST.get('landmark')
        pincode = request.POST.get('pincode')
        district = request.POST.get('district')
        capacity = request.POST.get('capacity')
        actype = request.POST.get('actype')
        rent = request.POST.get('rent')
        ac_rent = request.POST.get('ac_rent')
        non_ac_rent = request.POST.get('non_ac_rent')
        owner = request.POST.get('owner')
        contact = request.POST.get('contact')
        availability = request.POST.getlist('availability')
        feature = request.POST.getlist('feature')

        # Handle multiple image uploads
        images = request.FILES.getlist('image')  # Get list of uploaded images

        print("Uploaded images:", [image.name for image in images])  # Print uploaded image names

        # Create the Hall instance
        hall_save = Hall.objects.create(
            hallname=hallname,
            place=place,
            landmark=landmark,
            pincode=pincode,
            district=district,
            capacity=capacity,
            ac_nonac_both=actype,
            rent=rent,
            ac_rent=ac_rent,
            non_ac_rent=non_ac_rent,
            owner_name=owner,
            contact=contact,
            availability=availability,
            hall_feature=feature,
        )

        # Save features
        for feat in feature:
            Hallfeature.objects.create(
                hall=hall_save.id,
                feature=feat
            )

        # Save images to the Imagegallery table
        if images:  # Check if images list is not empty
            for myfile in images:
                Imagegallery.objects.create(hall=hall_save.id, image=myfile)  # Save each image

            print(f"Number of images saved: {len(images)}")  # Debugging: print number of images saved
        else:
            print("No images were uploaded.")

        # Process availability checkboxes
        availability_dict = {
            'sunday': 1 if 'Sun' in availability else 0,
            'monday': 1 if 'Mon' in availability else 0,
            'tuesday': 1 if 'Tue' in availability else 0,
            'wednesday': 1 if 'Wed' in availability else 0,
            'thursday': 1 if 'Thu' in availability else 0,
            'friday': 1 if 'Fri' in availability else 0,
            'saturday': 1 if 'Sat' in availability else 0,
        }
        Availability.objects.create(
            hall=hall_save,
            sunday=availability_dict['sunday'],
            monday=availability_dict['monday'],
            tuesday=availability_dict['tuesday'],
            wednessday=availability_dict['wednesday'],
            thursday=availability_dict['thursday'],
            friday=availability_dict['friday'],
            saturday=availability_dict['saturday'],
        )

        # Check total images saved
        total_images = Imagegallery.objects.filter(hall=hall_save).count()
        print(f"Total images for hall {hall_save.id}: {total_images}")

    feature_display = Feature.objects.exclude(isdelete=1)
    return render(request, 'hall.html', {'feature_display': feature_display})

def viewhall(request):
    hall_view=Hall.objects.exclude(isdelete=1)
    return render(request,'hallview.html',{'hall_view':hall_view})

def delete_hall(request, id):
    delete_hall = get_object_or_404(Hall, id=id)
    delete_hall.isdelete = 1
    delete_hall.delete()
    delete_hall.save()
    return HttpResponseRedirect(reverse(viewhall))

def updatehall(request,id):
    hall_update=get_object_or_404(Hall,id=id)
    feature_display = Feature.objects.exclude(isdelete=1)
    return render(request,'hall_update.html',{'hall_update':hall_update,'feature_display':feature_display})

def featuremanage(request):
    all_feature=Feature.objects.exclude(isdelete=1)
    update_feature=None
    if request.method=='POST':
        feature=request.POST.get('featurename')
        feature_id=request.POST.get('feature_id')
        if feature_id:
            try:
                update_feature=Feature.objects.get(id=feature_id)
                update_feature.featurename=feature
                update_feature.save()
            except Feature.DoesNotExist:
                pass
        else:
            update_feature=Feature(featurename=feature)
            update_feature.save()
        return redirect(featuremanage)
    return render(request,'hallfeature.html',{'allfeature':all_feature,'updatefeature':update_feature})

def update_feature(request, id): 
    try:
        update_feature = Feature.objects.get(id=id)
        return render(request, 'hallfeature.html',{
            'updatefeature': update_feature,
            'allfeature': Feature.objects.exclude(isdelete=1),
        })
    except Feature.DoesNotExist:
        return HttpResponseRedirect(reverse('featuremanage'))
    
def delete_feature(request, id):
    delete_feature = get_object_or_404(Feature, id=id)
    delete_feature.isdelete = 1
    delete_feature.delete()
    delete_feature.save()
    return HttpResponseRedirect(reverse(featuremanage))

def hallinoperabilitymanage(request):
    hallname_list = []
    all_hall=Hall.objects.exclude(isdelete=1)  
    all_inoperability=Inoperability.objects.exclude(isdelete=1)   
    update_inoperability=None
    if request.method=="POST":
        inoperability_id=request.POST.get('inoperability_id')
        hallname=request.POST.get('hallname')
        start=request.POST.get('startdate')
        end=request.POST.get('enddate')
        reason=request.POST.get('reason')
        if inoperability_id:
            try:
                update_inoperability=Inoperability.objects.get(id=inoperability_id)
                update_inoperability.hallname=hallname
                update_inoperability.start_date=start
                update_inoperability.end_date=end
                update_inoperability.reason=reason
                update_inoperability.save()
            except Feature.DoesNotExist:
                pass
        else:
            update_inoperability=Inoperability(hallname=hallname,start_date=start,end_date=end,reason=reason)
            update_inoperability.save()
        return redirect(hallinoperabilitymanage)
    # display saved hallid to hallname using list
 
    for inoperability in all_inoperability:
        hall= get_object_or_404(Hall, id=inoperability.hallname).hallname
        hallname_list.append({
            'id': inoperability.id,
            'start': inoperability.start_date,
            'end': inoperability.end_date,
            'reason': inoperability.reason,
            'hall':hall,
        })
    context={
        'allhall':all_hall,
        'allinoperability':all_inoperability,
        'halllist':hallname_list,
        'updateinoperability':update_inoperability,
        }
    return render(request,'hallinoperability.html',context)

def update_inoperability(request, id):
    try:
        # Get the inoperability object that we're updating
        update_inoperability = get_object_or_404(Inoperability, id=id)
        all_hall=Hall.objects.exclude(isdelete=1)  
        # Get all non-deleted inoperability records for display
        all_inoperability = Inoperability.objects.exclude(isdelete=1)

        # Prepare the hall name list for the dropdown
        hallname_list = []
        for inoperability in all_inoperability:
            hall = get_object_or_404(Hall, id=inoperability.hallname)
            hallname_list.append({
                'id': hall.id,
                'hallname': hall.hallname,
                'start': inoperability.start_date,
                'end': inoperability.end_date,
                'reason': inoperability.reason,
            })
        

        # Get the current hall name
        current_hall_name = get_object_or_404(Hall, id=update_inoperability.hallname).hallname

        # Render the template with the context
        return render(request, 'hallinoperability.html', {
            'updateinoperability': update_inoperability,
            'allinoperability': all_inoperability,
            'halllist': hallname_list,
            'current_hall_name': current_hall_name,
            'allhall':all_hall,
        })

    except Inoperability.DoesNotExist:
        return redirect('update_inoperability',id=id)
    
def delete_inoperability(request, id):
    delete_inoperability = get_object_or_404(Inoperability, id=id)
    delete_inoperability.isdelete = 1
    delete_inoperability.delete()
    delete_inoperability.save()
    return HttpResponseRedirect(reverse(hallinoperabilitymanage))

def paymentmanage(request):
    if request.method=="POST":
        paymentmode=request.POST.get('mode')
        total=request.POST.get('total')
        cash=request.POST.get('cash')
        remaining=request.POST.get('remaining')
        transaction=request.POST.get('transaction')
        payment_save=Payment(payment_mode=paymentmode,total_amount=total,cashreceived=cash,transaction_id=transaction,remaining_amount=remaining)
        payment_save.save()      
    return render(request,'hallpayment.html')

# def get_bookings(request,hall_id):
#     print("hall id :", hall_id)
#     if hall_id:
#         bookings = Booking.objects.filter(hallid=hall_id).values(
#             'name', 'date', 'timeslot', 'event_name', 'description', 'address', 'contact', 'ac'
#         )
#     else:
#         bookings = Booking.objects.all().values(
#             'name', 'date', 'timeslot', 'event_name', 'description', 'address', 'contact', 'ac'
#         )

#     # Format bookings as needed
#     event_list = []
#     for booking in bookings:
#         event_list.append({
#             'name': booking['name'],
#             'title': booking['event_name'],
#             'start': booking['date'].isoformat(),
#             'description': booking['description'],
#             'timeslot': booking['timeslot'],
#             'address': booking['address'],
#             'contact': booking['contact'],
#             'ac': booking['ac'],
#         })
#     print(event_list)
#     return JsonResponse(event_list, safe=False)

def get_bookings(request, hall_id):
    bookings = Booking.objects.filter(hallname=hall_id).values('name', 'date', 'timeslot', 'event_name', 'description', 'address', 'contact', 'ac','hallname')
    return JsonResponse(list(bookings), safe=False)

def calendarview(request):
    return render(request, 'calendar.html')

def cal(request):
    return render(request, 'hallcalendar.html')

def booked(request):
    Booked_list=Booking.objects.all()
    return render(request,'booklist.html',{'Booked_list':Booked_list})
 
def logout(request):
    return HttpResponseRedirect(reverse('adminlogin'))