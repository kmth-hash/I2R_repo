from django.shortcuts import render , redirect
from .models import Ingredients, Recipes , Category , Recipe_Ingredients , Users
from django.contrib import messages
from django.http import HttpResponse
from .test import storeDBfromCSV


def signup(request):    
    if request.method=='POST' :
        name = request.POST['first_name']+" "+request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['conf_password']

        if password==confirm_password:
            new_user = Users(username= name , password = password , height = "" , weight = "" , role = "user" )
            new_user.save()
            messages.success(request  , " Signup successful.")
            return redirect("/")
        else:
            messages.error(request  , " Password did not match.")
            return redirect("/signup")              
       

    return render(request , 'signup.html' , {})

def recipes(request):
    return render(request , 'recipes.html' , {})

def login(request):
    res = ''
    if request.method=='POST':
        name1 = request.POST['email']
        pass1 = request.POST['password']
        if '@' in name1:
            print('true @')            
            try:
                user_obj = Users.objects.get(email=name1,password = pass1)                
                res = user_obj
                messages.success(request , "Welcome back! Let's cook something good.")
                return redirect("/")
                
            except Exception as ex:
                messages.error(request , "Oops! Successfully Failed to login. You can do better. Cmon")
                return redirect("/")
        else:
            try:
                user_obj  = Users.objects.get(username = name1,password=pass1)
                res = user_obj
                messages.success(request , "Welcome back! Let's cook something good.")
                return redirect("/")        
                        
            except Exception as ex:
                messages.error(request , "Oops! Successfully Failed to login. You can do better. Cmon")
                return redirect("/")


    return render(request , 'login.html' , {})

def mainpage(request):
    return render(request , 'mainpage.html' , {})

def addRecipe(request):
    storeDBfromCSV()
    return render(request , 'addRecipe.html' , {})
def bmi(request):
    return render(request , 'bmi.html' , {})


