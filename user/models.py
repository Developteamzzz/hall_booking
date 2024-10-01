from django.db import models

class User(models.Model):

    name = models.CharField(max_length=100)
    number = models.IntegerField()
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    

    def __str__(self):
        return self.email


class User_OTP(models.Model):
    
    otp = models.IntegerField()
    is_verified = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True, blank=True)
    

class Hall(models.Model):
    
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    location = models.CharField(max_length=255, default="perumbavoor") 
    description = models.TextField(blank=True, null=True)
    amenities = models.CharField(max_length=255, blank=True, null=True)
    

    
    
    def __str__(self):
        return self.name
    
# class Hall(models.Model):
#     hallname=models.CharField(max_length=100)
#     place=models.CharField(max_length=100)
#     landmark=models.CharField(max_length=100)
#     capacity=models.CharField(max_length=100)
#     pincode=models.CharField(max_length=100)
#     district=models.CharField(max_length=100)
#     ac_nonac_both=models.CharField(max_length=100)
#     rent=models.CharField(max_length=100)
#     ac_rent=models.CharField(max_length=100)
#     non_ac_rent=models.CharField(max_length=100)
#     owner_name=models.CharField(max_length=100)
#     contact=models.CharField(max_length=100)
#     availability=models.CharField(max_length=100)
#     images=models.CharField(max_length=100)
#     hall_feature=models.CharField(max_length=100)
#     addedon=models.DateField(auto_now_add=True)
#     isdelete=models.IntegerField(default=0)
#     addedby=models.IntegerField(default=0)


class Booking(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, null=True, blank=True,default=1)
    date = models.CharField(max_length=100)
    timeslot = models.CharField(max_length=10)
    description = models.CharField(max_length=100, default='')
    ac = models.BooleanField()
    approval_status = models.BooleanField()
    added_on = models.DateTimeField(auto_now_add=True)
    program = models.CharField(max_length=100)
    evening_before = models.CharField(max_length=3,default="no",null=True)
    features = models.TextField()



# class Booking(models.Model):
#     name=models.CharField(max_length=100)
#     address=models.CharField(max_length=100)
#     contact=models.CharField(max_length=100)
#     date = models.DateField()
#     timeslot=models.CharField(max_length=100)
#     ac=models.CharField(max_length=100)
#     description=models.CharField(max_length=100)
#     event_name=models.CharField(max_length=100)
#     addedon=models.DateField(auto_now_add=True)
#     approval_status=models.CharField(max_length=100)
#     hallname=models.CharField(max_length=100)


class Feature(models.Model):
    name = models.CharField(max_length=255)
    addedon=models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

# class Feature(models.Model):
#     featurename=models.CharField(max_length=100)
#     addedby=models.IntegerField(default=0)
#     addedon=models.DateField(auto_now_add=True)
#     isdelete=models.IntegerField(default=0)

# class Availability(models.Model):
#     hall=models.CharField(max_length=100)
#     sunday=models.IntegerField(default=0)
#     monday=models.IntegerField(default=0)
#     tuesday=models.IntegerField(default=0)
#     wednessday=models.IntegerField(default=0)
#     thursday=models.IntegerField(default=0)
#     friday=models.IntegerField(default=0)
#     saturday=models.IntegerField(default=0)
#     addedon=models.DateField(auto_now_add=True)
#     isdelete=models.IntegerField(default=0)
#     addedby=models.IntegerField(default=0)

class HallFeature(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    addedon=models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Feature {self.feature.id} for Hall {self.hall.id}"

# class Hallfeature(models.Model):
#     hall=models.CharField(max_length=100)
#     feature=models.CharField(max_length=100)
#     addedby=models.IntegerField(default=0)
#     addedon=models.DateField(auto_now_add=True)
#     isdelete=models.IntegerField(default=0)

class HallImage(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hall_images/')
    addedon=models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Image for Hall {self.hall.id}"
    
# class Imagegallery(models.Model):
#     hall=models.CharField(max_length=100)
#     image=models.CharField(max_length=100)
#     addedby=models.IntegerField(default=0)
#     addedon=models.DateField(auto_now_add=True)
#     isdelete=models.IntegerField(default=0)


# class Inoperability(models.Model):
#     hallname=models.CharField(max_length=100, null=False)
#     start_date=models.CharField(max_length=100)
#     end_date=models.CharField(max_length=100)
#     reason=models.CharField(max_length=100)
#     addedby=models.IntegerField(default=0)
#     addedon=models.DateField(auto_now_add=True)
#     isdelete=models.IntegerField(default=0)




