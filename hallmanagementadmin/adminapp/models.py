from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField()
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=250)


class User_OTP(models.Model):
    otp = models.IntegerField()
    is_verified = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    
class Adminrecord(models.Model):
    username=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    addedon=models.DateField(auto_now_add=True)
    superadmin=models.IntegerField(default=0)
    isdelete=models.IntegerField(default=0)

class Feature(models.Model):
    featurename=models.CharField(max_length=100)
    addedby=models.IntegerField(default=0)
    addedon=models.DateField(auto_now_add=True)
    isdelete=models.IntegerField(default=0)

class Availability(models.Model):
    hall=models.CharField(max_length=100)
    sunday=models.IntegerField(default=0)
    monday=models.IntegerField(default=0)
    tuesday=models.IntegerField(default=0)
    wednessday=models.IntegerField(default=0)
    thursday=models.IntegerField(default=0)
    friday=models.IntegerField(default=0)
    saturday=models.IntegerField(default=0)
    addedon=models.DateField(auto_now_add=True)
    isdelete=models.IntegerField(default=0)
    addedby=models.IntegerField(default=0)

class Discount(models.Model):
    discount=models.CharField(max_length=100)
    addedby=models.IntegerField(default=0)
    addedon=models.DateField(auto_now_add=True)
    isdelete=models.IntegerField(default=0)

class Hall(models.Model):
    hallname=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    landmark=models.CharField(max_length=100)
    capacity=models.CharField(max_length=100)
    pincode=models.CharField(max_length=100)
    district=models.CharField(max_length=100)
    ac_nonac_both=models.CharField(max_length=100)
    rent=models.CharField(max_length=100)
    ac_rent=models.CharField(max_length=100)
    non_ac_rent=models.CharField(max_length=100)
    owner_name=models.CharField(max_length=100)
    contact=models.CharField(max_length=100)
    availability=models.CharField(max_length=100)
    images=models.CharField(max_length=100)
    hall_feature=models.CharField(max_length=100)
    addedon=models.DateField(auto_now_add=True)
    isdelete=models.IntegerField(default=0)
    addedby=models.IntegerField(default=0)

class Hallfeature(models.Model):
    hall=models.CharField(max_length=100)
    feature=models.CharField(max_length=100)
    addedby=models.IntegerField(default=0)
    addedon=models.DateField(auto_now_add=True)
    isdelete=models.IntegerField(default=0)

class Imagegallery(models.Model):
    hall=models.CharField(max_length=100)
    image=models.CharField(max_length=100)
    addedby=models.IntegerField(default=0)
    addedon=models.DateField(auto_now_add=True)
    isdelete=models.IntegerField(default=0)

class Inoperability(models.Model):
    hallname=models.CharField(max_length=100, null=False)
    start_date=models.CharField(max_length=100)
    end_date=models.CharField(max_length=100)
    reason=models.CharField(max_length=100)
    addedby=models.IntegerField(default=0)
    addedon=models.DateField(auto_now_add=True)
    isdelete=models.IntegerField(default=0)

class Member(models.Model):
    role=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    addedby=models.IntegerField(default=0)
    addedon=models.DateField(auto_now_add=True)
    isdelete=models.IntegerField(default=0)

class Payment(models.Model):
    payment_mode=models.CharField(max_length=100)
    transaction_id=models.CharField(max_length=100)
    total_amount=models.CharField(max_length=100)
    cashreceived=models.CharField(max_length=100)
    remaining_amount=models.CharField(max_length=100)
    booking_id=models.IntegerField()
    addedby=models.IntegerField(default=0)
    addedon=models.DateField(auto_now_add=True)
    isdelete=models.IntegerField(default=0)

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    contact=models.CharField(max_length=100)
    date = models.DateField()
    timeslot=models.CharField(max_length=100)
    ac=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    event_name=models.CharField(max_length=100)
    addedon=models.DateField(auto_now_add=True)
    approval_status=models.CharField(max_length=100)
    hallname=models.CharField(max_length=100)
    evening_before = models.CharField(max_length=3,default="no",null=True)
    features = models.TextField()