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
    return render(request , 'login.html' , {})

def mainpage(request):
    return render(request , 'mainpage.html' , {})

def addRecipe(request):
    storeDBfromCSV()
    return render(request , 'addRecipe.html' , {})