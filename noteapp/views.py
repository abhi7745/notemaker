from django.shortcuts import render

# importing password encryptor
from django.contrib.auth.hashers import make_password, check_password

# importing all app models
from noteapp.models import *

# importing django login athentications
from django.contrib.auth import authenticate, login, logout

# it is for filter only logined user can access user dashboard page
from django.contrib.auth.decorators import login_required

# Create your views here.

# home page
def index(request):
    if request.user.is_authenticated:
        print('User Already logined')
        notevalue=note.objects.filter(email__contains=request.user) # this data is for showing note data in pages
        return render(request,'user_dashboard.html',{'notevalue':notevalue})

    return render(request,'index.html',{})

# both signup & login page for input data
# def login_signup(request):
#     return render(request,'login_signup.html',{}) cancelled view

# signup logic
def signup(request):
    if request.user.is_authenticated:
        print('User Already logined')
        notevalue=note.objects.filter(email__contains=request.user) # this data is for showing note data in pages
        return render(request,'user_dashboard.html',{'notevalue':notevalue})
    else:
        if request.method=='POST':
            email=request.POST.get('signup_email')
            password=request.POST.get('signup_password')
            confirm_psd=request.POST.get('signup_confirm_psd')
            print(email)
            print(password)
            print('signup form')


            if(email== '' or password==''):
                print('No value')
                return render(request,'login_signup.html',{'checker':'Please enter valid info...!','static_data':email})

            elif(not password==confirm_psd):
                print('Password Missmatch')
                return render(request,'login_signup.html',{'checker':'password Missmatch...!','static_data':email})
            
            elif(not email.endswith('@gmail.com')):
                print('Invalid Email...!')
                return render(request,'login_signup.html',{'checker':'Invalid Email...!','static_data':email})
            
            elif User.objects.filter(username=email).exists():
                print('User already exist')
                return render(request,'login_signup.html',{'checker':'User already exist..!.','static_data':email})

            else:  
                #making password encryption for login purpose(becz django weak password is not allowed in authentication)
                passEncrypted = make_password(password)
                
                # creating User table object
                auth_user=User()
                auth_user.username=email
                auth_user.password=passEncrypted
                auth_user.save()
                return render(request,'login_signup.html',{'checker':'Account Created Successfully.. Please Login..!'})

    return render(request,'login_signup.html',{})

# login logic
def loginpage(request):
    notevalue=note.objects.filter(email__contains=request.user) # this data is for showing note data in pages
    if request.user.is_authenticated:
        print('User Already logined')
        return render(request,'user_dashboard.html',{'notevalue':notevalue})
    else:
        if request.method=='POST':
            email=request.POST.get('email')
            password=request.POST.get('password')
            print(email)
            print(password)
            print('login form')

            if(email== '' or password==''):
                print('No value')
                return render(request,'login_signup.html',{'checker':'Please enter valid info...!','static_mail':email})

            elif(not email.endswith('@gmail.com')):
                print('Invalid Email...!')
                return render(request,'login_signup.html',{'checker':'Invalid Email...!','static_mail':email})

            else:
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    login(request, user)
                    print('user login success')
                    notevalue=note.objects.filter(email__contains=request.user) # this data is for showing note data in pages
                    return render(request,'user_dashboard.html',{'notevalue':notevalue})
                else:
                    return render(request,'login_signup.html',{'checker':'Invalid Username or Password','static_mail':email})

    
    return render(request,'login_signup.html',{})


# user dashboard page logic and user saving data note code is here
@login_required(login_url="/login")
def user_dashboard(request): # user saving data code is here
    notevalue=note.objects.filter(email__contains=request.user) # this data is for global
    for x in notevalue:
        print(x.data,'my values')

    if request.method=='POST':
        notedata=request.POST.get('notedata')
        # print(notedata)

        if (notedata == ''):
            print('No value')
            return render(request,'user_dashboard.html',{'checker':'Please enter valid data...!','notevalue':notevalue})

        elif ( len(notedata)>100 ):
            print('Limit 100 Crossed')
            return render(request,'user_dashboard.html',{'checker':'You cross the limit of data (100 above characters reached)...!','notevalue':notevalue})

        # condition for filtering same content. main thing is " 1. individual user cannot save duplicate datas in one account(only edit or delete)
        #  2. user can save same data of other user data list(eg: if sumon have the data 'hello' and moncy have the same data 'hello') -
        #  in this condition the both user can save the same data only once.  "
        elif note.objects.filter(email=request.user,data=notedata).exists():
            print('same data found')
            return render(request,'user_dashboard.html',{'checker':'Same data found in your note...! Please Edit or Delete Your Note',
            'notevalue':notevalue})

        else:
            user_db=User.objects.filter(username__contains=request.user)
            for userid in user_db:
                print(userid.id,'Userid')
            
            note_db=note()
            note_db.login_id=userid #saving User id to note db
            note_db.data=notedata
            note_db.email=request.user
            note_db.save()

            notevalue=note.objects.filter(email__contains=request.user) # Fetching new data fron note db
            return render(request,'user_dashboard.html',{'checker':'Note saved succesfully..','notevalue':notevalue})


    # notevalue=note.objects.filter(email__contains=request.user)

    return render(request,'user_dashboard.html',{'notevalue':notevalue})

def update(request,pk):


    if request.method=='POST':
        notedata=request.POST.get('note')
        notedb=note.objects.get(u_id=pk)
        print(notedb.data)

        if (notedata == ''):
            print('No value')
            return render(request,'update.html',{'updatemsg':'Please enter valid data...!','pk':pk,'notedb':notedb})

        elif ( len(notedata)>100 ):
            print('Limit 100 Crossed')
            return render(request,'update.html',{'updatemsg':'You cross the limit of data (100 above characters reached)...!',
            'pk':pk,'notedb':notedb})
        
        # condition for filtering same content. main thing is " 1. individual user cannot save duplicate datas in one account(only edit or delete)
        #  2. user can save same data of other user data list(eg: if sumon have the data 'hello' and moncy have the same data 'hello') -
        #  in this condition the both user can save the same data only once.  "
        elif note.objects.filter(email=request.user,data=notedata).exists():
            print('same data found')
            return render(request,'update.html',{'checker':'Same data found in your note...! Please Edit or Delete Your Note',
            'pk':pk,'notedb':notedb})

        else:
            #  reassign and update value
            notedb.data=notedata
            notedb.save()
            return render(request,'update.html',{'pk':pk,'notedb':notedb,'updatemsg':'Succesfully Updated'})

    notedb=note.objects.get(u_id=pk)
    return render(request,'update.html',{'pk':pk,'notedb':notedb})


def delete(request,pk):
    notedb=note.objects.get(u_id=pk)
    print(notedb.data)
    notedb.delete()
    print('Note delete successfully')
    
    notevalue=note.objects.filter(email__contains=request.user) # this data is for global
    return render(request,'user_dashboard.html',{'notevalue':notevalue})

def logoutpage(request):
    logout(request)
    return render(request,'index.html',{})


