from django.db import models
from django.contrib.auth.models import User


class User_OTP(models.Model):
    
    otp = models.IntegerField()
    is_verified = models.BooleanField()
    
    
class User(models.Model):

    name = models.CharField(max_length=100)
    number = models.IntegerField()
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    user_otp = models.ForeignKey(User_OTP, on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return self.email



class Hall(models.Model):
    
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    location = models.CharField(max_length=255, default="perumbavoor") 
    description = models.TextField(blank=True, null=True)
    amenities = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
    
   
# class UserContact(models.Model):
#     name = models.CharField(max_length=100)
#     number = models.CharField(max_length=15)
#     address = models.TextField()
#     email = models.EmailField()
#     otp = models.CharField(max_length=6, blank=True, null=True)
#     is_verified = models.BooleanField(default=False)

#     def __str__(self):
#         return self.name
   
    
# class Booking(models.Model):
#     hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
#     start_time = models.DateTimeField()
#     end_time = models.DateTimeField()
#     user_contact = models.ForeignKey(UserContact, on_delete=models.CASCADE)
#     event_type = models.CharField(max_length=50)
#     event_details = models.CharField(max_length=255, blank=True)  # Can keep for reference if needed
#     event_description = models.TextField(blank=True)
#     ac = models.BooleanField()
#     approval_status = models.BooleanField()
#     added_on = models.DateTimeField(auto_now_add=True)
#     timeslot = models.CharField(max_length=10)

#     def __str__(self):
#         return f"{self.hall.name} booked for {self.event_type}"
    
    
class Booking(models.Model):
    
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # hall_id = models.ForeignKey(Hall, on_delete=models.CASCADE)
    date = models.CharField(max_length=100)
    timeslot = models.CharField(max_length=10)
    description = models.CharField(max_length=100, default='')
    ac = models.BooleanField()
    approval_status = models.BooleanField()
    added_on = models.DateTimeField(auto_now_add=True)

