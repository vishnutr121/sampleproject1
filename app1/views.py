from django.shortcuts import render,redirect
from django.contrib.auth.hashers import check_password
from .models import Categories,Pet,Petcart,Donor,Customer,SalesCount,HomePets
import random
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
import os
import re
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

def homepage(req):
    if req.user.is_authenticated:
        if req.user.is_superuser:
            return redirect('adminhome')
        else:
            if Customer.objects.filter(user=req.user):
                return redirect('customerhome')
            else:
                return redirect('donorhome')
    cat=Categories.objects.all()
    pets=Pet.objects.filter(buystatus='Not Sold',approval='true')
    homepets1=HomePets.objects.all()
    homepets1.delete()
    for i in pets:
        homepets2=HomePets(home_pet_name=i.pet_name,home_price=i.price,home_pet_image=i.pet_image,offer_percent=random.randint(10,30))
        homepets2.save()
    homepets3=HomePets.objects.all()
    return render(req,'homepage.html',{'category':cat,'homepets3':homepets3})

@login_required(login_url='homepage')
def adminhome(req):
    if not req.user.is_superuser:
        if Customer.objects.filter(user=req.user):
            return redirect('customerhome')
        else:
            return redirect('donorhome')
    don=Donor.objects.all()
    cus=Customer.objects.all()
    pet1=Pet.objects.filter(buystatus='Sold')
    pet2=Pet.objects.filter(approval='false')
    c1,c2,c3,c4=0,0,0,0
    for i in don:
        c1+=1
    for i in cus:
        c2+=1
    for i in pet1:
        c3+=1
    for i in pet2:
        c4+=1
    return render(req,'adminhome.html',{'c1':c1,'c2':c2,'c3':c3,'c4':c4})

@login_required(login_url='homepage')
def customerhome(req):
    if req.user.is_superuser:
        return redirect('adminhome')
    else:
        if Donor.objects.filter(user=req.user):
            return redirect('donorhome')
    usr22=Customer.objects.get(user=req.user.id)
    return render(req,'customerhome.html',{'usr22':usr22})

@login_required(login_url='homepage')
def donorhome(req):
    if req.user.is_superuser:
        return redirect('adminhome')
    else:
        if Customer.objects.filter(user=req.user):
            return redirect('customerhome')
    usr22=Donor.objects.get(user=req.user.id)
    don=Donor.objects.get(user=req.user)
    pets=Pet.objects.filter(donor=don,buystatus='Sold')
    salescount=SalesCount.objects.get(user=req.user.id)
    salescount.olddisapprove=salescount.newdisapprove
    salescount.oldsales=salescount.sales
    c1=0
    for i in pets:
        c1+=1
    salescount.sales=c1
    newsales=c1-salescount.oldsales
    salescount.save()
    count=0
    disapprovedpets=Pet.objects.filter(donor=don,approval='disapprove')
    for i in disapprovedpets:
        count+=1
    salescount.newdisapprove=count
    newdis=count-salescount.olddisapprove
    salescount.save()
    return render(req,'donorhome.html',{'usr22':usr22,'c2':c1,'newsales':newsales,'disa_count':count,'newdis':newdis})

def donorsignup(req):
    if req.user.is_authenticated:
        if req.user.is_superuser:
            return redirect('adminhome')
        else:
            if Customer.objects.filter(user=req.user):
                return redirect('customerhome')
            else:
                return redirect('donorhome')
    return render(req,'donorsignup.html')

def customersignup(req):
    if req.user.is_authenticated:
        if req.user.is_superuser:
            return redirect('adminhome')
        else:
            if Customer.objects.filter(user=req.user):
                return redirect('customerhome')
            else:
                return redirect('donorhome')
    return render(req,'customersignup.html')

def add_cus(req):
    if req.user.is_authenticated:
        if req.user.is_superuser:
            return redirect('adminhome')
        else:
            if Customer.objects.filter(user=req.user):
                return redirect('customerhome')
            else:
                return redirect('donorhome')
    if req.method=='POST':
        fn=req.POST['cfname']
        ln=req.POST['clname']
        uname=req.POST['cusername']
        em=req.POST['cemail']
        ph=req.POST['cphone']
        add=req.POST['caddress']
        image=req.FILES.get('img1')
        pass1 = str(random.randint(100000, 999999))
        if User.objects.filter(username=uname).exists():
            messages.info(req,'This username already exists!!!')
            return redirect('customersignup')
        elif User.objects.filter(email=em).exists():
            messages.info(req,'This email already exists!!!')
            return redirect('customersignup')
        else:    
            user=User.objects.create_user (
            first_name=fn,
            last_name=ln,
            username=uname,
            password=pass1,
            email=em)
            user.save()
            usmem=Customer(user=user,address=add,phone_number=ph,image=image)
            usmem.save()
            sub='Login Details'
            message="Your Login details are:\nUsername:{}\nPassword:{}\nPlease reset your password after login. Thank You.".format(uname,pass1)
            send_mail(sub,message,settings.EMAIL_HOST_USER,[em])
            messages.info(req,'Please check your mail for login details...')
        return redirect('homepage')
    else:
        return render(req,'customersignup.html')
    
def add_don(req):
    if req.user.is_authenticated:
        if req.user.is_superuser:
            return redirect('adminhome')
        else:
            if Customer.objects.filter(user=req.user):
                return redirect('customerhome')
            else:
                return redirect('donorhome')
    if req.method=='POST':
        fn=req.POST['dfname']
        ln=req.POST['dlname']
        uname=req.POST['dusername']
        em=req.POST['demail']
        ph=req.POST['dphone']
        add=req.POST['daddress']
        image=req.FILES.get('img1')
        pass1 = str(random.randint(100000, 999999))
        if User.objects.filter(username=uname).exists():
            messages.info(req,'This username already exists!!!')
            return redirect('donorsignup')
        elif User.objects.filter(email=em).exists():
            messages.info(req,'This email already exists!!!')
            return redirect('donorsignup')
        else:    
            user=User.objects.create_user (
            first_name=fn,
            last_name=ln,
            username=uname,
            password=pass1,
            email=em)
            user.save()
            usmem=Donor(user=user,address=add,phone_number=ph,image=image)
            usmem.save()
            salescount=SalesCount(user=user,sales=0,oldsales=0)
            salescount.save()
            sub='Login Details'
            message="Your Login details are:\nUsername:{}\nPassword:{}\nPlease reset your password after login. Thank You.".format(uname,pass1)
            send_mail(sub,message,settings.EMAIL_HOST_USER,[em])
            messages.info(req,'Please check your mail for login details...')
        return redirect('homepage')
    else:
        return render(req,'donorsignup.html')

def login1(req):
    if req.method == 'POST':
        username1 = req.POST['usrname']
        password1 = req.POST['pwd']
        user = auth.authenticate(username=username1, password=password1)
        don1=Donor.objects.filter(user=user)
        cus1=Customer.objects.filter(user=user)
        if user is not None:
            if don1:
                login(req, user)
                return redirect('donorhome')
            elif cus1:
                login(req, user)
                return redirect('customerhome')
            else:
                login(req, user)
                return redirect('adminhome')
        else:
            messages.info(req, 'Invalid username or password! Try Again...')
            return redirect('homepage')
    else:
        return redirect('homepage')

def logout(req):
    auth.logout(req)
    return redirect('homepage')

@login_required(login_url='homepage')
def editadminprofile(req):
    if not req.user.is_superuser:
        if Customer.objects.filter(user=req.user):
            return redirect('customerhome')
        else:
            return redirect('donorhome')
    user=req.user.id
    usr=User.objects.get(id=user)
    return render(req,'editadminprofile.html',{'usr':usr})

def edit_admin_details(req):
    if not req.user.is_superuser:
        if Customer.objects.filter(user=req.user):
            return redirect('customerhome')
        else:
            return redirect('donorhome')
    if req.method=='POST':
        user=User.objects.get(id=req.user.id)
        user.first_name=req.POST['ufname']
        user.last_name=req.POST['ulname']
        user.username=req.POST['uusrname']
        user.email=req.POST['uemail']
        user.save()
        messages.info(req, 'User details updates successfully...')
        return redirect('editadminprofile')
    return render(req,'editadminprofile.html')

@login_required(login_url='homepage')
def resetadminpassword(req):
    if not req.user.is_superuser:
        if Customer.objects.filter(user=req.user):
            return redirect('customerhome')
        else:
            return redirect('donorhome')
    return render(req,'resetadminpassword.html')

def edit_admin_password(req):
    if not req.user.is_superuser:
        if Customer.objects.filter(user=req.user):
            return redirect('customerhome')
        else:
            return redirect('donorhome')
    if req.method=='POST':
        user=User.objects.get(id=req.user.id)
        pass1=req.POST['oldpass']
        pass2=req.POST['pass1']
        pass3=req.POST['pass2']
        if check_password(pass1, user.password):
            if pass2==pass3:
                user.set_password(pass2)
                user.save()
                auth.logout(req)
                messages.info(req, 'Password updated successfully. Please Log in with new password...')
                return redirect('homepage')
            else:
                messages.info(req, 'Passwords not matching! Try again...')
                return redirect('resetadminpassword')
        else:
            messages.info(req, 'Passwords not matching! Try again...')
            return redirect('resetadminpassword')
    return render(req,'resetadminpassword.html')

@login_required(login_url='homepage')
def donordetails(req):
    if not req.user.is_superuser:
        if Customer.objects.filter(user=req.user):
            return redirect('customerhome')
        else:
            return redirect('donorhome')
    don=Donor.objects.all()
    return render(req,'donordetails.html',{'don':don})

@login_required(login_url='homepage')
def customerdetails(req):
    if not req.user.is_superuser:
        if Customer.objects.filter(user=req.user):
            return redirect('customerhome')
        else:
            return redirect('donorhome')
    cus=Customer.objects.all()
    return render(req,'customerdetails.html',{'cus':cus})

@login_required(login_url='homepage')
def view_don(req,pid):
    if not req.user.is_superuser:
        if Customer.objects.filter(user=req.user):
            return redirect('customerhome')
        else:
            return redirect('donorhome')
    don=Donor.objects.get(id=pid)
    return render(req,'viewdonor.html',{'don':don})

@login_required(login_url='homepage')
def view_cus(req,pid):
    if not req.user.is_superuser:
        if Customer.objects.filter(user=req.user):
            return redirect('customerhome')
        else:
            return redirect('donorhome')
    cus=Customer.objects.get(id=pid)
    return render(req,'viewcustomer.html',{'cus':cus})

def delete_don(req,pid):
    don=Donor.objects.get(id=pid)
    user = User.objects.get(id=don.user.id)
    don.delete()
    user.delete()
    return redirect('donordetails')

def delete_cus(req,pid):
    cus=Customer.objects.get(id=pid)
    user = User.objects.get(id=cus.user.id)
    cus.delete()
    user.delete()
    return redirect('customerdetails')

@login_required(login_url='homepage')
def view_cat(req):
    if not req.user.is_superuser:
        if Customer.objects.filter(user=req.user):
            return redirect('customerhome')
        else:
            return redirect('donorhome')
    cat=Categories.objects.all()
    return render(req,'categorydetails.html',{'cat':cat})

@login_required(login_url='homepage')
def edit_cat(req,pid):
    if not req.user.is_superuser:
        if Customer.objects.filter(user=req.user):
            return redirect('customerhome')
        else:
            return redirect('donorhome')
    cat=Categories.objects.get(id=pid)
    return render(req,'editcategory.html',{'cat':cat})

@login_required(login_url='homepage')
def add_cat(req):
    if not req.user.is_superuser:
        if Customer.objects.filter(user=req.user):
            return redirect('customerhome')
        else:
            return redirect('donorhome')
    return render(req,'addcategory.html')

def delete_cat(req,pid):
    cat=Categories.objects.get(id=pid)
    cat.delete()
    return redirect('view_cat')

def add_cat_details(req):
    if not req.user.is_superuser:
        if Customer.objects.filter(user=req.user):
            return redirect('customerhome')
        else:
            return redirect('donorhome')
    if req.method=='POST':
        catname=req.POST['catname']
        img=req.FILES.get('img1')
        cat=Categories(category_name=catname,category_image=img)
        cat.save()
        return redirect('view_cat')
    return render(req,'addcategory.html')

def edit_cat_details(req,pid):
    if not req.user.is_superuser:
        if Customer.objects.filter(user=req.user):
            return redirect('customerhome')
        else:
            return redirect('donorhome')
    if req.method=='POST':
        cat=Categories.objects.get(id=pid)
        cat.category_name=req.POST['cname']
        if len(req.FILES)!=0:
            if len(cat.category_image)>0:
                os.remove(cat.category_image.path)
            cat.category_image=req.FILES.get('imgfile')
        cat.save()
        return redirect('view_cat')
    return render(req,'editcategory.html')

@login_required(login_url='homepage')
def edit_don(req):
    if req.user.is_superuser:
        return redirect('adminhome')
    else:
        if Customer.objects.filter(user=req.user):
            return redirect('customerhome')
    user=req.user
    usr22=Donor.objects.get(user=req.user.id)
    usr=Donor.objects.get(user=user)
    salescount=SalesCount.objects.get(user=req.user.id)
    c2=salescount.sales
    count=0
    disapprovedpets=Pet.objects.filter(donor=usr,approval='disapprove')
    for i in disapprovedpets:
        count+=1
    return render(req,'editdonor.html',{'usr':usr,'usr22':usr22,'c2':c2,'disa_count':count})

@login_required(login_url='homepage')
def edit_don_details(req):
    if req.method=='POST':
        usr=Donor.objects.get(user=req.user)
        usr2=User.objects.get(id=req.user.id)
        usr2.first_name=req.POST['ufname']
        usr2.last_name=req.POST['ulname']
        usr2.username=req.POST['uusrname']
        usr2.email=req.POST['uemail']
        usr.phone_number=req.POST['uphone']
        usr.address=req.POST['uaddress']
        if len(req.FILES)!=0:
            if len(usr.image)>0:
                os.remove(usr.image.path)
            usr.image=req.FILES.get('imgfile')
        usr.save()
        usr2.save()
        messages.info(req, 'Details updates successfully...')
        return redirect('edit_don')
    return render(req,'editdonor.html')

@login_required(login_url='homepage')
def resetdonorpassword(req):
    if req.user.is_superuser:
        return redirect('adminhome')
    else:
        if Customer.objects.filter(user=req.user):
            return redirect('customerhome')
    usr22=Donor.objects.get(user=req.user.id)
    salescount=SalesCount.objects.get(user=req.user.id)
    c2=salescount.sales
    count=0
    disapprovedpets=Pet.objects.filter(donor=usr22,approval='disapprove')
    for i in disapprovedpets:
        count+=1
    return render(req,'resetdonorpassword.html',{'usr22':usr22,'c2':c2,'disa_count':count})

def edit_donor_password(req):
    if req.method=='POST':
        user=User.objects.get(id=req.user.id)
        pass1=req.POST['oldpass']
        pass2=req.POST['pass1']
        pass3=req.POST['pass2']
        if check_password(pass1, user.password):
            if pass2==pass3:
                user.set_password(pass2)
                user.save()
                auth.logout(req)
                messages.info(req, 'Password updated successfully. Please Log in with new password...')
                return redirect('homepage')
            else:
                messages.info(req, 'Passwords not matching! Try again...')
                return redirect('resetdonorpassword')
        else:
            messages.info(req, 'Passwords not matching! Try again...')
            return redirect('resetdonorpassword')
    return render(req,'resetdonorpassword.html')

@login_required(login_url='homepage')
def donatepet(req):
    if req.user.is_superuser:
        return redirect('adminhome')
    else:
        if Customer.objects.filter(user=req.user):
            return redirect('customerhome')
    usr22=Donor.objects.get(user=req.user.id)
    category = Categories.objects.all()
    salescount=SalesCount.objects.get(user=req.user.id)
    c2=salescount.sales
    count=0
    disapprovedpets=Pet.objects.filter(donor=usr22,approval='disapprove')
    for i in disapprovedpets:
        count+=1
    return render(req, 'donatepet.html', {'category': category,'usr22':usr22,'c2':c2,'disa_count':count})

def donate_pet_function(req):
    if req.method == 'POST':
        usr = req.user
        don = Donor.objects.get(user=usr)
        pet_name = req.POST['petname']
        pet_desc = req.POST['petdescription']
        pet_price = req.POST['petprice']
        image = req.FILES.get('img1')
        sel = req.POST.get('sel', 'default')
        if sel == 'default':
            messages.error(req, 'Please select a valid category.')
            return redirect('donatepet')
        else:
            category = Categories.objects.get(id=sel)
            pet = Pet(category=category, approval='false', buystatus='Not Sold', donor=don, pet_name=pet_name,
                      pet_description=pet_desc, price=pet_price, pet_image=image)
            pet.save()
            messages.info(req, 'New entry will be seen in donated pets after approval...')
            return redirect('donatepet')
    return render(req, 'donatepet.html')

@login_required(login_url='homepage')
def donatedpets(req):
    if req.user.is_superuser:
        return redirect('adminhome')
    else:
        if Customer.objects.filter(user=req.user):
            return redirect('customerhome')
    usr=req.user
    usr22=Donor.objects.get(user=req.user.id)
    don=Donor.objects.get(user=usr)
    pets=Pet.objects.filter(donor=don,approval='true',buystatus='Not Sold')
    salescount=SalesCount.objects.get(user=req.user.id)
    c2=salescount.sales
    count=0
    disapprovedpets=Pet.objects.filter(donor=don,approval='disapprove')
    for i in disapprovedpets:
        count+=1
    return render(req,'donatedpets.html',{'pets':pets,'usr22':usr22,'c2':c2,'disa_count':count})

@login_required(login_url='homepage')
def editpet(req,pid):
    if req.user.is_superuser:
        return redirect('adminhome')
    else:
        if Customer.objects.filter(user=req.user):
            return redirect('customerhome')
    usr22=Donor.objects.get(user=req.user.id)
    category=Categories.objects.all()
    pet=Pet.objects.get(id=pid)
    salescount=SalesCount.objects.get(user=req.user.id)
    c2=salescount.sales
    a=random.randint(123212,994359)
    pet.captcha=a
    pet.save()
    count=0
    disapprovedpets=Pet.objects.filter(donor=usr22,approval='disapprove')
    for i in disapprovedpets:
        count+=1
    return render(req,'editpet.html',{'pet':pet,'category':category,'usr22':usr22,'c2':c2,'a':a,'disa_count':count})

def edit_pet_function(req,pid):
    if req.method=='POST':
        usr=req.user
        pet=Pet.objects.get(id=pid)
        pet.donor=Donor.objects.get(user=usr)
        pet.pet_name=req.POST['petname']
        pet.price=req.POST['petprice']
        sel=req.POST['sel']
        pet.category=Categories.objects.get(id=sel)
        pet.pet_description=req.POST['petdescription']
        if len(req.FILES)!=0:
            if len(pet.pet_image)>0:
                os.remove(pet.pet_image.path)
            pet.pet_image=req.FILES.get('imgfile')
        if pet.captcha==int(req.POST['captcha']):
            pet.save()
            messages.info(req, 'Details updated successfully...')
            return redirect('donatedpets')
        else:
            messages.info(req, 'Invalid captcha!!!')
            return redirect('donatedpets')
    return render(req,'editpet.html')

def delete_pet(req,pid):
    pet=Pet.objects.get(id=pid)
    pet.delete()
    return redirect('donatedpets')

@login_required(login_url='homepage')
def adminnotifications(req):
    if not req.user.is_superuser:
        if Customer.objects.filter(user=req.user):
            return redirect('customerhome')
        else:
            return redirect('donorhome')
    pet=Pet.objects.filter(approval='false')
    if pet:
        count=1
    return render(req,'adminnotifications.html',{'pet':pet})

def approve_pet(req,pid):
    if not req.user.is_superuser:
        if Customer.objects.filter(user=req.user):
            return redirect('customerhome')
        else:
            return redirect('donorhome')
    pet=Pet.objects.get(id=pid)
    pet.approval='true'
    pet.save()
    return redirect('adminnotifications')

def disapprove_pet(req,pid):
    if not req.user.is_superuser:
        if Customer.objects.filter(user=req.user):
            return redirect('customerhome')
        else:
            return redirect('donorhome')
    pet=Pet.objects.get(id=pid)
    pet.approval='disapprove'
    pet.save()
    return redirect('adminnotifications')

@login_required(login_url='homepage')
def edit_cus(req):
    if req.user.is_superuser:
        return redirect('adminhome')
    else:
        if Donor.objects.filter(user=req.user):
            return redirect('donorhome')
    usr22=Customer.objects.get(user=req.user.id)
    user=req.user
    usr=Customer.objects.get(user=user)
    return render(req,'editcustomer.html',{'usr':usr,'usr22':usr22})

def edit_cus_details(req):
    if req.method=='POST':
        usr=Customer.objects.get(user=req.user)
        usr2=req.user.id
        user=User.objects.get(id=usr2)
        user.first_name=req.POST['ufname']
        user.last_name=req.POST['ulname']
        user.username=req.POST['uusrname']
        user.email=req.POST['uemail']
        usr.phone_number=req.POST['uphone']
        usr.address=req.POST['uaddress']
        if len(req.FILES)!=0:
            if len(usr.image)>0:
                os.remove(usr.image.path)
            usr.image=req.FILES.get('imgfile')
        usr.save()
        user.save()
        messages.info(req, 'Details updates successfully...')
        return redirect('edit_cus')
    return render(req,'editcustomer.html')

@login_required(login_url='homepage')
def resetcustomerpassword(req):
    if req.user.is_superuser:
        return redirect('adminhome')
    else:
        if Donor.objects.filter(user=req.user):
            return redirect('donorhome')
    usr22=Customer.objects.get(user=req.user.id)
    return render(req,'resetcustomerpassword.html',{'usr22':usr22})

def edit_customer_password(req):
    if req.method=='POST':
        user=User.objects.get(id=req.user.id)
        pass1=req.POST['oldpass']
        pass2=req.POST['pass1']
        pass3=req.POST['pass2']
        if check_password(pass1, user.password):
            if pass2==pass3:
                user.set_password(pass2)
                user.save()
                auth.logout(req)
                messages.info(req, 'Password updated successfully. Please Log in with new password...')
                return redirect('homepage')
            else:
                messages.info(req, 'Passwords not matching! Try again...')
                return redirect('resetcustomerpassword')
        else:
            messages.info(req, 'Passwords not matching! Try again...')
            return redirect('resetcustomerpassword')
    return render(req,'resetcustomerpassword.html')

@login_required(login_url='homepage')
def pets_available(req):
    if req.user.is_superuser:
        return redirect('adminhome')
    else:
        if Donor.objects.filter(user=req.user):
            return redirect('donorhome')
    usr22=Customer.objects.get(user=req.user.id)
    category=Categories.objects.all()
    return render(req,'allcategories.html',{'category':category,'usr22':usr22})

@login_required(login_url='homepage')
def category_pets(req,pid):
    if req.user.is_superuser:
        return redirect('adminhome')
    else:
        if Donor.objects.filter(user=req.user):
            return redirect('donorhome')
    usr22=Customer.objects.get(user=req.user.id)
    category=Categories.objects.get(id=pid)
    pet=Pet.objects.filter(category=category,approval='true',buystatus='Not Sold')
    return render(req,'categorypets.html',{'pet':pet,'usr22':usr22})

def buypet(req,pid):
    cus = Customer.objects.get(user=req.user)
    pet = Pet.objects.get(id=pid)
    pet.buystatus='Sold'
    pet.customer=cus
    pet.save()
    pcart = Petcart(pet=pet,customer=cus.user)
    pcart.save()
    return redirect('petsbought')

@login_required(login_url='homepage')
def petsbought(req):
    if req.user.is_superuser:
        return redirect('adminhome')
    else:
        if Donor.objects.filter(user=req.user):
            return redirect('donorhome')
    usr22=Customer.objects.get(user=req.user.id)
    pets=Petcart.objects.filter(customer=req.user)
    return render(req,'petsbought.html',{'pets':pets,'usr22':usr22})

@login_required(login_url='homepage')
def donornotifications(req):
    if req.user.is_superuser:
        return redirect('adminhome')
    else:
        if Customer.objects.filter(user=req.user):
            return redirect('customerhome')
    usr22=Donor.objects.get(user=req.user.id)
    don=Donor.objects.get(user=req.user)
    pets=Pet.objects.filter(donor=don,buystatus='Sold',pets_view='false')
    for i in pets:
        i.pets_view='true'
        i.save()
    salescount=SalesCount.objects.get(user=req.user.id)
    c2=salescount.sales
    count=0
    disapprovedpets=Pet.objects.filter(donor=don,approval='disapprove')
    for i in disapprovedpets:
        count+=1
    return render(req,'donornotifications.html',{'pets':pets,'usr22':usr22,'c2':c2,'disa_count':count})

@login_required(login_url='homepage')
def purchasedetails(req):
    if not req.user.is_superuser:
        if Customer.objects.filter(user=req.user):
            return redirect('customerhome')
        else:
            return redirect('donorhome')
    pet=Pet.objects.filter(buystatus='Sold')
    return render(req,'purchasedetails.html',{'pet':pet})

@login_required(login_url='homepage')
def donationdetails(req):
    if not req.user.is_superuser:
        if Customer.objects.filter(user=req.user):
            return redirect('customerhome')
        else:
            return redirect('donorhome')
    pet=Pet.objects.filter(approval='true')
    return render(req,'donationdetails.html',{'pet':pet})

@login_required(login_url='homepage')
def petdetails(req,pid):
    if req.user.is_superuser:
        return redirect('adminhome')
    else:
        if Donor.objects.filter(user=req.user):
            return redirect('donorhome')
    usr22=Customer.objects.get(user=req.user.id)
    pet=Pet.objects.get(id=pid)
    return render(req,'petdetails.html',{'pet':pet,'usr22':usr22})

def individualdonationdetails(req,pid):
    don=Donor.objects.get(id=pid)
    pet=Pet.objects.filter(donor=don,approval='true')
    return render(req,'individualdonationdetails.html',{'pet':pet})

def disapprovedpets(req):
    don=Donor.objects.get(user=req.user)
    pet=Pet.objects.filter(donor=don,approval='disapprove')
    count=0
    disapprovedpets=Pet.objects.filter(donor=don,approval='disapprove')
    for i in disapprovedpets:
        count+=1
    return render(req,'disapprovedpets.html',{'pet':pet,'usr22':don,'disa_count':count})

def donorsoldpets(req):
    don=Donor.objects.get(user=req.user)
    pet=Pet.objects.filter(donor=don,buystatus='Sold')
    count=0
    disapprovedpets=Pet.objects.filter(donor=don,approval='disapprove')
    for i in disapprovedpets:
        count+=1
    return render(req,'donorsoldpets.html',{'pet':pet,'usr22':don,'disa_count':count})