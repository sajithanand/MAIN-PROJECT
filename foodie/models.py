from django.db import models

# Create your models here.

class login(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    user_type = models.CharField(max_length=20, null=True)
    
class user(models.Model):
    l_id=models.ForeignKey(login,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    gender=models.CharField(max_length=100)
    dob=models.DateField()
    email=models.CharField(max_length=100)
    phone=models.BigIntegerField()
    
class restaurant(models.Model):
    l_id=models.ForeignKey(login,on_delete=models.CASCADE)
    rname=models.CharField(max_length=1000)
    address=models.CharField(max_length=1000)
    details=models.CharField(max_length=1000)
    time1=models.CharField(max_length=100)
    time2=models.CharField(max_length=100)
    image=models.FileField()
    license_image=models.CharField(max_length=100)
    phone_number=models.BigIntegerField()
    email=models.CharField(max_length=1000)
    lattitude=models.CharField(max_length=100)
    longitude=models.CharField(max_length=100)
    rating=models.CharField(max_length=100)
   
class facility_table(models.Model):
    rest_id=models.ForeignKey(restaurant,on_delete=models.CASCADE)
    facility=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    image=models.FileField()
    
class food_type(models.Model):
    rest_id=models.ForeignKey(restaurant,on_delete=models.CASCADE)
    type=models.CharField(max_length=100)
    description=models.CharField(max_length=2000)
    image=models.FileField()
    class Meta:
        unique_together = ('rest_id', 'type',)

    

    
    
class food_item(models.Model):
    type_id=models.ForeignKey(food_type,on_delete=models.CASCADE)
    item=models.CharField(max_length=100)
    price=models.FloatField(default=0.0)
    description=models.CharField(max_length=2000)
    image=models.FileField()
    status=models.CharField(max_length=100)
    category=models.CharField(max_length=100)
    class Meta:
        unique_together = ('type_id', 'item',)
    
    
    
    
    
    
class feeback(models.Model):
    uid=models.ForeignKey(user,on_delete=models.CASCADE)
    Date=models.CharField(max_length=200)
    feed=models.CharField(max_length=200)
    
class complaint(models.Model):
    uid=models.ForeignKey(user,on_delete=models.CASCADE)
    rest_id=models.ForeignKey(restaurant,on_delete=models.CASCADE)
    complaint=models.CharField(max_length=200)
    reply=models.CharField(max_length=200)
    Date=models.DateField(max_length=200)
    
    
class review(models.Model):
    rest_id=models.ForeignKey(restaurant,on_delete=models.CASCADE)
    uid=models.ForeignKey(user,on_delete=models.CASCADE)
    review=models.CharField(max_length=200)
    Date=models.DateField(max_length=200)
    image=models.ImageField(max_length=200)
    rating1=models.CharField(max_length=100)
    rating2=models.CharField(max_length=100)
    
    
    

    
    
    
        

