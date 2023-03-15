from datetime import datetime
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import * 
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import requests




#Web scrapping
def web_scrapping(h_name):
    print("https://restaurant-guru.in/"+h_name+"/reviews/google")
    res = requests.get("https://restaurant-guru.in/"+h_name+"/reviews/google").text
    res_rating=res.split('<div class="fill ag_sel"')[1].split(">")[0].split(": ")[1].split("%")[0]
    print(res_rating)
    t_rating=(int(res_rating)*5)/100
    


    print(t_rating)
    print('+++++++++++++++++++++++++++++++++')



    res_comments=res.split('<div id="comments_container"')[1].split("data-id=")

    reviews=[]

    for i in range(1,len(res_comments)):
        try:
            r=res_comments[i]
            name=r.split('class="user_info__name"')[1].split('>')[1].split("<")[0]
            # print(name)
            rating=int(r.split('style="width: ')[1].split('%;')[0])*5/100
            # print(rating)
            review=r.split('class="text_full">')[1].split("<")[0]
            # print(review)
            print("======================")
            img="1star.png"
            if(float(rating)<=1):
                img="1star.png"
            elif (float(rating)<=2):
                img="2star.png"
            elif (float(rating)<=2.5):
                img="2.5star.png"
            elif (float(rating)<=3.0):
                img="3star.jpg"
            elif (float(rating)<=3.5):
                img="3.5star.png"
            elif (float(rating)<=4.0):
                img="4star.png"
                
            elif (float(rating)<=4.5):
                img="4.5.png"
                
            else:
                img="5star.png"
            row={"name":name,"rating":rating,"review":review,"img":img}
            reviews.append(row)
        except:
            pass
    res1=requests.get("https://restaurant-guru.in/"+h_name).text
    # print(res1)
    imgs_res=res1.split('class="swiper-wrapper')[1]
    imgs_res=imgs_res.split('<img width="')
    images=[]
    for i in range(1,len(imgs_res)):
        img=imgs_res[i]
        img=img.split('src="')[1].split('"')[0]
        print(img)
        if "jpg" in img or 'png' in img or "jpeg" in img:
            images.append(img)
            if(len(images)==3):
                break
    return t_rating,reviews,images
# Create your views here.

def index(request):
    return render(request,'home/index.html')


def about(request):
    return render(request,'home/about.html')

def service(request):
    return render(request,'home/service.html')


#Login page
def login_page(request):
    return render(request,'Login.html')


#Login
def user_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            users = login.objects.get(username = username,password = password)
        except:
            return HttpResponse('''<script>alert("login failed");window.location="/"</script>''')
        
        checkUser = users.username==username
        checkPassword = users.password==password
        
        if users and checkUser and checkPassword :
            request.session['l_id'] = users.id
            
        
            if users.user_type == 'admin':
                return redirect('admin_home')
           
            
            elif users.user_type == 'user': 
                request.session['l_id']=users.id
                request.session['username']=user.objects.get(l_id=users.id).name
                return redirect('user_hom')  
               
            elif users.user_type == 'restaurant':
                request.session['l_id'] = users.id
                request.session['restname']=restaurant.objects.get(l_id=users.id).rname
                return redirect('restaurant_home')  
            
            else:
                return HttpResponse('''<script>alert("Login failed");window.location="/"</script>''')
            
        
        else:
            return redirect('login_page')
            
            
            

        
        
#Admin Home
def admin_home(request):
    try:
        user = login.objects.get(pk = request.session['l_id'])
    except:
        return
    if user.user_type == 'admin':
        return render(request,'admin/home.html')
    else:
        return redirect('Login_page')
    
    
    
#Admin home
def home_page(request):
    return render(request,'admin/home.html')
    
#Verify restaurants
def verify_restaurants(request):
    
    from django.db.models import Case, When, IntegerField

    # ob = restaurant.objects.annotate(l_id__user_type=Case(When(demo_field='accepted', then=1), default=0, output_field=IntegerField())).order_by('l_id__user_type')
    ob=restaurant.objects.all().order_by('id').reverse()
    return render(request,'admin/verify_restaurant.html',{'val':ob})   

# order_by(status='accepted').values()                  


def accept(request,id):
    ob=login.objects.get(id=id)
    ob.user_type='restaurant'
    ob.save()
    get_restaurent = restaurant.objects.get(l_id = id)
    # print(get_restaurent.email)
    subject = 'Restaurent verification'
    message = 'Your request has accepted'
    recipient = get_restaurent.email
    send_mail(subject,message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
    messages.success(request, 'Success!')
    return HttpResponse('''<script>alert("Restaurants accepted");window.location="/verify_restaurants"</script>''')

def rejected(request,id):
    ob=login.objects.get(id=id)
    ob.user_type='reject'
    ob.save()
    get_restaurant = restaurant.objects.get(l_id = id)
    subject = 'Restaurant verification'
    message = 'Your request has been declined '
    recipient = get_restaurant.email
    send_mail(subject,message, settings.EMAIL_HOST_USER, [recipient], fail_silently=False)
    messages.success(request, 'Success!')
    return HttpResponse('''<script>alert("Restaurants rejected");window.location="/verify_restaurants"</script>''')


#View More Details
def view_more(request,id):
    ob=restaurant.objects.get(id=id)
    request.session['l_id'] = id
    return render(request, 'admin/view_details.html',{'val':ob})


    

 
        
    

    
    
##User registration  
def user_register(request):
    return render(request,'new_register.html')

def reg(request):
    name=request.POST['name']
    address=request.POST['address']
    dob=request.POST['birthday']
    email=request.POST['username']
    number=request.POST['phone']

    password=request.POST['password']
    gender=request.POST['gender']
    
    ob=login()
    ob.username = email
    ob.password = password
    ob.user_type = "user"
    ob.save()
    
    ob1=user()
    ob1.l_id=ob
    ob1.name=name
    ob1.address=address
    ob1.gender=gender
    ob1.dob=dob
    ob1.email=email
    ob1.phone=number
    ob1.save()
    return HttpResponse('''<script>alert("Registration successfull");window.location="user_hom"</script>''')




    
    
    

##User Home
def home(request):
    return render(request,'user/user_home.html',{'name':request.session['username']})



def user_hom(request):
    try:
        user = login.objects.get(pk = request.session['l_id'])
    except:
        return
    
    if user.user_type == 'user':
        request.l_id__id=request.session['l_id']
        return render(request,'user/log.html',{'name':request.session['username']})
    else:
        return redirect('login_page')
    
def user_update(request):
    ob=user.objects.get(l_id__id=request.session['l_id'])
    d=str(ob.dob)
    print(ob,"=======================================")
    return render(request,'user/update_profile.html',{'val':ob,'d':d,'name':request.session['username']})
 
def use_update(request):
    name=request.POST['name']
    address=request.POST['address']
    dob=request.POST['birthday']
    email=request.POST['email']
    number=request.POST['number']
    gender=request.POST['gender']
    
    ob=user.objects.get(l_id__id=request.session['l_id'])
    ob.name=name
    ob.address=address
    ob.gender=gender
    ob.dob=dob
    ob.email=email
    ob.phone=number
    ob.save()
    return HttpResponse('''<script>alert("Profile updated successfully");window.location="user_hom"</script>''')
    
    
    
    
##Restaurant registration
def restaurant_reg(request):
    return render(request,'restaurant/regsiter.html')


def rest_reg(request):
    name=request.POST['name']
    address=request.POST['address']
    details=request.POST['details']
    image=request.FILES['files']
    fn=FileSystemStorage()
    fs=fn.save(image.name,image)
    license=request.POST['license']
    timea=request.POST['TIME1']
    timeb=request.POST['TIME2']
    number=request.POST['number']
    username=request.POST['email']
    password=request.POST['Password']
    
    ob=login()
    ob.username = username
    ob.password = password
    ob.user_type = "pending"
    ob.save()
    
    ob2=restaurant()
    ob2.l_id=ob
    ob2.rname=name
    ob2.address=address
    ob2.details=details
    ob2.time1=timea
    ob2.time2=timeb
    ob2.image=fs
    ob2.license_image=license
    ob2.phone_number=number
    ob2.lattitude="0"
    ob2.longitude="0"
    ob2.save()
    request.session['locid']=ob2.id
    return HttpResponse('''<script>alert("Registration successfull Select Location");window.location="/map"</script>''')



#Map function
def map(request):
    
    return render(request,"restaurant/map.html")


#Map function
def map1(request):
    lat=request.POST['lat']
    lon=request.POST['lon']
    ob=restaurant.objects.get(id=request.session['locid'])
    ob.lattitude=lat
    ob.longitude=lon
    ob.save()
    return HttpResponse('''<script>alert("Registration Completed");window.location="/"</script>''')






#Restaurant home
def restaurant_home(request):
    try:
        user = login.objects.get(pk = request.session['l_id'])
    except:
        return
    
    if user.user_type == 'restaurant':
        request.session['l_id']=user.id
        return render(request,'restaurant/homepage.html',{'rest_name':request.session['restname']})
    else:
        return redirect('login_page')
    
    
    
#restaurant home
def rest_home(request):
    return render(request,'restaurant/homepage.html',{'rest_name':request.session['restname']})
    
        
#Restaurant update profile
def res_update(request):
    ob1=restaurant.objects.get(l_id__id=request.session['l_id'])
    print(ob1,"=======================================")
    return render(request,'restaurant/profile-update.html',{'val':ob1,'rest_name':request.session['restname']})

def update(request):
   
    Address=request.POST['Address']
    Details=request.POST['details']
    Time1=request.POST['TIME1']
    number=request.POST['license']
    print(number,"*********************************************")
    Time2=request.POST['TIME2']
    phone=request.POST['phony']
    
    images=request.FILES['file']
    fn=FileSystemStorage()
    fs=fn.save(images.name,images)
    
    ob1=restaurant.objects.get(l_id__id=request.session['l_id'])
    
    ob1.address=Address
    ob1.details=Details
    ob1.time1=Time1
    ob1.time2=Time2
    ob1.license_image=number
    ob1.phone_number=phone
    ob1.image=fs

    ob1.save()
    return HttpResponse('''<script>alert("Profile updated successfully");window.location="restaurant_home"</script>''')

#Restaurant add facility
def add_facility(request):
    return render(request,'restaurant/add_facility.html',{'rest_name':request.session['restname']})


def add_facili(request):
    facility=request.POST['textfield']
    descriptio=request.POST['textfield2']
    image=request.FILES['file']
    fn=FileSystemStorage()
    fs=fn.save(image.name,image)

    
    ob2=facility_table()
    ob2.facility=facility
    ob2.description=descriptio
    ob2.rest_id=restaurant.objects.get(l_id__id=request.session['l_id'])
    ob2.image=fs
    ob2.save()
    return HttpResponse('''<script>alert("Facility successfully added");window.location="restaurant_home"</script>''')


#Restaurant manage facility
def manage(request):
    ob=facility_table.objects.filter(rest_id__l_id__id=request.session['l_id'])       #View function
    return render(request,'sample1.html',{'val':ob,'rest_name':request.session['restname']})


#Delete facility details
def delete(request,id):
    ob=facility_table.objects.get(id=id)
    ob.delete()                                 ############################DELETE FUNCTION#######################################
    return HttpResponse('''<script>alert("Facility deleted");window.location="/manage"</script>''')
    
    
    
#ADD food types
def add_food(request):
    return render(request,'restaurant/ADD_food_types.html',{'rest_name':request.session['restname']})


def add_food_type(request):
    try:
        typ=request.POST['name']
        descriptio=request.POST['description']
        imag=request.FILES['file']
        fn=FileSystemStorage()
        fs=fn.save(imag.name,imag)
        ob2=food_type()
        ob2.type=typ
        ob2.description=descriptio
        ob2.image=fs
        ob2.rest_id=restaurant.objects.get(l_id__id=request.session['l_id'])
        ob2.save()
        return HttpResponse('''<script>alert(" Food type added successfully");window.location="manage_foodtype"</script>''')
    
    except:
        return HttpResponse('''<script>alert("Could not add duplicate types");window.location="manage_foodtype"</script>''')
        


#Manage food types
def manage_foodtype(request):
    ob=food_type.objects.filter(rest_id__l_id__id=request.session['l_id'])       
    return render(request,'restaurant/manage_foodtype.html',{'val':ob,'rest_name':request.session['restname']})

#Edit Food Types
def edit_foodtypes(request,id):
    ob=food_type.objects.get(id=id)
    request.session['fdid']=id
    return render(request,'restaurant/edit_foodtypes.html',{'val':ob,'rest_name':request.session['restname']})


def edit(request):
    type=request.POST['textfield']
    description=request.POST['textfield2']
    images=request.FILES['file']
    fn=FileSystemStorage()
    fs=fn.save(images.name,images)
    
    ob1=food_type.objects.get(id=request.session['fdid'])
    ob1.type=type
    ob1.description=description
    ob1.image=fs

    ob1.save()
    return HttpResponse('''<script>alert("Details edited successfully");window.location="/restaurant_home"</script>''')



#Delete Food types
def delete_foodtype(request,id):
    ob1=food_type.objects.get(id=id)
    ob1.delete()                                 
    return HttpResponse('''<script>alert("food type deleted");window.location="/manage_foodtype"</script>''')




#Manage_food_item
def manage_item(request):
    ob1=food_type.objects.filter(rest_id__l_id=request.session['l_id'])
    return render(request,'restaurant/manage_fooditem.html',{'val1':ob1,'rest_name':request.session['restname']})




#dropdown 
def getitem(request):
    type=request.POST['select']
    print(type)
    ob=food_item.objects.filter(type_id__id=type) 
    ob1=food_type.objects.filter(rest_id__l_id=request.session['l_id'])
    return render(request,'restaurant/manage_fooditem.html',{'val2':ob,'val1':ob1,'rest_name':request.session['restname']})
    
    
#Add Food items
def add_item(request):
    ob=food_type.objects.filter(rest_id__l_id=request.session['l_id'])
    return render(request,'restaurant/add_fooditem.html',{'val1':ob,'rest_name':request.session['restname']})             ##Add food item page



#Add food item1
def add_fooitem(request):
    
    
    fdtype=request.POST['select']
    print(fdtype)
    item1=request.POST['item']
    price1=request.POST['Price']
    description1=request.POST['description']
    imag=request.FILES['file']
    category=request.POST['select1']
    
    try:
        fn=FileSystemStorage()
        fs=fn.save(imag.name,imag)
        ob2=food_item()
        ob2.item=item1
        ob2.price=price1
        ob2.category=category
        ob2.image=fs
        ob2.description=description1
        ob2.type_id=food_type.objects.get(id=fdtype)
        ob2.status='available'
        ob2.rest_id=restaurant.objects.get(l_id__id=request.session['l_id'])
        ob2.save()
        return HttpResponse('''<script>alert("Food item added successfully");window.location="/manage_item"</script>''')
        
    except:
        return HttpResponse('''<script>alert("Could not add duplicate items");window.location="/manage_item"</script>''')
       


#Edit food_item
def edit_fooditem(request,id):
    ob1=food_item.objects.get(id=id)
    request.session['ftid']=id
    return render(request,'restaurant/edit_fooditem.html',{'val':ob1,'rest_name':request.session['restname']})


def edit_food(request):
    catego=request.POST['select1']
    item=request.POST['name']
    price=request.POST['Price']
    descri=request.POST['desc']
    status=request.POST['status']
    images=request.FILES['file']
    fn=FileSystemStorage()
    fs=fn.save(images.name,images)
    
    ob2=food_item.objects.get(id=request.session['ftid'])
    ob2.item=item
    ob2.price=price
    ob2.description=descri
    ob2.status=status
    ob2.category=catego
    ob2.image=fs

    ob2.save()
    return HttpResponse('''<script>alert("Details edited successfully");window.location="/manage_item"</script>''')



#Delete food_item
def delete_item(request,id):
    ob=food_item.objects.get(id=id)
    ob.delete()                                
    return HttpResponse('''<script>alert("food item is deleted");window.location="/manage_item"</script>''')

#View restaurants by user
def view_restaurants(request):
    ob=restaurant.objects.all()
    return render(request,'user/View_restaurants.html',{'val':ob,'name':request.session['username']}) 

#Searching
def search(request):
    txt=request.POST['txt']
    from django.db import connection
    cursor=connection.cursor()
    sen_res=[]
    cursor.execute("SELECT * FROM `foodie_restaurant` WHERE `address` LIKE '%"+str(txt)+"%'")
    res=cursor.fetchall()
    print(res,"==========================")
    data = []
    for a in res:
        row = {"id":a[0], "rname": a[1], "address": a[2], "details": a[3],"time1":a[4],"time2":a[6], "image":a[6], "license_image":a[7], "phone_number":a[8], "email":a[9], "lattitude":a[10], "longitude":a[11]}
        data.append(row)
    return render(request,'user/View_restaurants.html',{'val':data,'name':request.session['username']}) 


#web scrapping  
def web_scrapping1(request,id):
    ob=restaurant.objects.get(id=id)
    print(ob)
    rating,reviews,images=web_scrapping(ob.rname)
    return render(request,'user/View_resdetails.html',{'val':ob})

#View_rest details
def viewresults(request,id):
    
    ob1=restaurant.objects.all()
    hotel = restaurant.objects.get(id = id)
    rating,reviews,images = web_scrapping(hotel.rname)
    print(images)
    print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    img0=images[0]
    img1=images[1]
    img2=images[2]
    rat=float(rating)
    img="1star.png"
    if(float(rating)<=1):
        img="1star.png"
    elif (float(rating)<=2):
        img="2.0star.png"
    elif (float(rating)<=2.5):
        img="2.5star.png"
    elif (float(rating)<=3.0):
        img="3star.png"
    elif (float(rating)<=3.5):
        img="3.5star.png"
    elif (float(rating)<=4.0):
        img="4star.png"
        
    elif (float(rating)<=4.5):
        img="4.5.png"
        
    else:
        img="5star.png"
    
    return render(request,'user/View_resdetails.html',{'rating':rat,"ri":img,'review':reviews,"img0":img0,"img1":img1,"img2":img2,"name":hotel.rname,'count':len(reviews),'details':hotel.details,'address':hotel.address,'time1':hotel.time1,'time2':hotel.time2})
    
    
    
    
#Feedback sending
def feedback(request):
    return render(request,'user/send_feednack.html')



def feedback1(request):
    feedback=request.POST['textfield']
    
    ob2=feeback()
    ob2.feed=feedback
    ob2.Date=datetime.today()
    ob2.uid=user.objects.get(l_id__id=request.session['l_id'])
    ob2.save()
    return HttpResponse('''<script>alert("feedback added successfully");window.location="/home"</script>''')



#View feedback function
def view_feedback(request):
    ob=feeback.objects.all()
    return render(request,'admin/View_feedback.html',{'val':ob,}) 


#Compliant sending
def get_rest(request):
    
    ob1=restaurant.objects.all()
    return render(request,'user/send_compalit.html',{'val':ob1})


def send_complaint(request):
    rest=request.POST['restaurants']
    compliant=request.POST['compliant']
    
    ob2=complaint()
    ob2.uid=user.objects.get(l_id__id=request.session['l_id'])
    ob2.complaint=compliant
    ob2.Date=datetime.today()
    ob2.reply='pending'
    ob2.rest_id=restaurant.objects.get(id=rest)
    ob2.save()
    return HttpResponse('''<script>alert("Compliant sended");window.location='/user_hom'</script>''')


#View Compliant
def view_compliant(request):
    ob=complaint.objects.all()
    return render(request,'admin/Compalint.html',{'val':ob})


#Send reply  
def reply(request,id):
    request.session['comp_id']=id
    return render(request,'admin/send_replay.html')

#send reply
def reply1(request):
    reply=request.POST['textfield']
    
    ob=complaint.objects.get(id=request.session['comp_id'])
    ob.reply=reply
    ob.save()
    return HttpResponse('''<script>alert("reply sended");window.location='/view_compliant'</script>''')


#View replay
def View_reply(request):
    ob=complaint.objects.filter(uid__l_id__id=request.session['l_id'])
    return render(request,'user/View_replay.html',{'val':ob})







    
    
    
    

    



    