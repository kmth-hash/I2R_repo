from django.shortcuts import render




def signup(request):
    return render(request , 'signup.html' , {})

def login(request):
    return render(request , 'login.html' , {})

def mainpage(request):
    return render(request , 'mainpage.html' , {})

def bmi(request):
    return render(request , 'bmi.html' , {})


