from django.shortcuts import render , redirect
from .models import Ingredients, Recipes , Category , Recipe_Ingredients , Users
from django.contrib import messages
from django.http import HttpResponse
from .test import storeDBfromCSV
from .add_ons import *

from json import loads,dumps
from django.core.files.storage import FileSystemStorage
# from keras import preprocessing
# import matplotlib.pyplot as plt
import os
# import yolov5
from django.db import connection
import numpy as np
# from keras.models import load_model
# from keras import backend as K
from itertools import chain
from collections import Counter,OrderedDict
imagesToPreview = []
datajson = []
name_of_the_recipe=[]
fats=[]
calories=[]
quantity=[]
proteins=[]
isLoggedIn = False
username = ''
recipe_json=[]
recipes_array = []
carbohydrates=[]
description=[]
# names = ['Tomato','cauli']
procedure=[]
predcited_items=[]
# from pathlib import Path
# fd=exec(Path("yolov5/detect.py").read_text())
# print(fd)
# print(gh)
def profile(request):
    return render(request,'profile.html')
def signupprofile(request):
    return render(request,'signupprofile.html')
def firstcall(request):
    return redirect('/home')
def predict(iurl):
    global predcited_items
    toexecute = 'python yolov5/detect.py --weights probably_the_last_one.pt --img 640 --conf 0.1 --source '
    jh=[]
    toexecute+=iurl
    gh=os.system(toexecute)
    with open('predictions.txt','r') as f:
        for line in f:
            jh.append(line.strip())
            if line.strip() not in predcited_items:
                predcited_items.append(str(line.strip()).title())
    print(predcited_items)
    return jh
def signup(request):
    global isLoggedIn      
    if request.method=='POST' :
        name = request.POST['first_name']+" "+request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['conf_password']

        if password==confirm_password:
            new_user = Users(username= name , password = password , height = "" , weight = "" , role = "user", email=email )
            new_user.save()
            request.session['username'] = name
            isLoggedIn = True
            messages.success(request  , " Signup successful.")
            return redirect("/")
        else:
            messages.error(request  , " Password did not match.")
            return redirect("/signup")
    return render(request , 'signup.html' , {})
def recipes(request):
    recipe_string = ''
    if not request.session.has_key('username'):
        return redirect('/login')
    global imagesToPreview,recipes_array,predcited_items
    a=[]
    recipes_array=[]
    imagesToPreview = loads(request.POST['hiddeninput'])
    print(imagesToPreview)
    for j,i in enumerate(predcited_items):
        if len(predcited_items)>1:
            if j == len(predcited_items)-1:
                recipe_string +=i
            else:
                recipe_string +=i+', '
        else:
            recipe_string = i
        with connection.cursor() as cursor:
            cursor.execute('SELECT "Receipe_Id_id" FROM myproj_recipe_ingredients WHERE "Ingredient_Id_id"=(SELECT "Ingredient_id" FROM myproj_ingredients WHERE "name"=%s)',[i])
            row = cursor.fetchall()
            item = []
            for j in row:
                item.append(list(j)[0])
            a.append(item)
        connection.close()
    x = Counter(chain.from_iterable(a))
    y = OrderedDict(x.most_common()) 
    final_recipe_list = list(y.keys())
    for recipe_id in final_recipe_list:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM myproj_recipes WHERE "Receipe_Id"=%s',[recipe_id])
            row = cursor.fetchall()
            item = []
            for j in row:
                # print(list(j))
                recipe_details = {
                    'name':list(j)[1],
                    'fats':list(j)[2],
                    'calories':list(j)[3],
                    'quantity':list(j)[4],
                    'proteins':list(j)[5],
                    'carbohydrates':list(j)[6],
                    'imageURL':list(j)[7],
                    'description':list(j)[8],
                    'procedure':list(j)[9]
                }
                recipes_array.append(recipe_details)
        connection.close()
    recipe_json = dumps(recipes_array)
    return render(request , 'recipes.html' , {'recipe_data':recipe_json,'predcited_items':recipe_string,'username':username})

def login(request):
    global isLoggedIn
    res = ''
    if request.method=='POST':

        name1 = request.POST['email']
        pass1 = request.POST['password']
        
        if '@' in name1:                     
            try:
                user_obj = Users.objects.get(password=pass1  , email=name1)                
                res = user_obj
                isLoggedIn = True
                request.session['username'] = user_obj.username
                messages.success(request , "Welcome back! Let's cook something good.")
                return redirect("/" , isLoggedIn = True , username = user_obj.username)
                
            except Exception as ex:
                
                isLoggedIn = False
                messages.error(request , "Oops! Successfully Failed to login. You can do better. Cmon")
                return redirect("/login" )
        else:
            try:
                user_obj  = Users.objects.get(username = name1,password=pass1)
                res = user_obj
                isLoggedIn = True
                request.session['username'] = user_obj.username
                messages.success(request , "Welcome back! Let's cook something good.")
                return redirect("/" , isLoggedIn = True , username = user_obj.username)  
                        
            except Exception as ex:
                isLoggedIn = False
                messages.error(request , "Oops! Successfully Failed to login. You can do better. Cmon")
                return redirect("/login")

    return render(request , 'login.html' , {})
def logout(request):
    global isLoggedIn,username,datajson
    try:
        del request.session['username']
        isLoggedIn = False
        username = ''
        imagesToPreview=[]
        datajson=[]
        messages.success(request , 'Successfully Logged out')
    except:
        messages.error(request , 'Error while logging out')
        #print('Error in clearing session')
    #return render(request , 'mainpage.html' , { 'isLoggedIn' : False , 'username' : '' })
    return redirect('/')

def mainpage(request):
    if not request.session.has_key('username'):
        return redirect('/login')
    global imagesToPreview,datajson
    if request.POST:
        if request.POST['Name']:
            imagesToPreview = loads(request.POST['hiddeninput'])
            print("sdfgdf")
            print(imagesToPreview)
            image_text = request.POST['Name']
            uploaded_file_url = '/static/assets/img/veg/'+str(image_text).lower()+'.jpg'
            imageAndName = {
                'imageURL':uploaded_file_url,
                'name':image_text
            }
            # predictedNames.append(predictedImage)
            predcited_items.append(str(image_text).title())
            imagesToPreview.append(imageAndName)
            datajson = dumps(imagesToPreview)
        else:

            imagesToPreview = loads(request.POST['hiddeninput'])
            print("sdfgdf")
            print(imagesToPreview)
            doc = request.FILES #returns a dict-like object
            doc_name = doc['image']
            fs = FileSystemStorage()
            filename = fs.save(doc_name.name, doc_name)
            uploaded_file_url = fs.url(filename)
            predictedImage = predict(str(uploaded_file_url)[1:])
            imageAndName = {
                'imageURL':uploaded_file_url,
                'name':predictedImage
            }
            # predictedNames.append(predictedImage)
            imagesToPreview.append(imageAndName)
            datajson = dumps(imagesToPreview)
    return render(request , 'mainpage.html' , {'len':len(imagesToPreview),'imagesToPreview':imagesToPreview,'data':datajson , 'isLoggedIn' : isLoggedIn , 'username' : username })

def addRecipe(request):
    all_recipe_percentage = return_recipes(['egg' , 'onion' , 'butter' , 'salt', 'pepper'])
    #valid_recipes = find_valid_recipes(all_recipe_percentage)
    print(all_recipe_percentage)
    return render(request , 'addRecipe.html' , {})

def bmi(request):
    if not request.session.has_key('username'):
        return redirect('/login')
    global isLoggedIn
    username = ''
    weight = 0
    height = 0
    if request.session.has_key('username'):
        username = setUserName(request.session['username'])
        user_obj = Users.objects.get( username = request.session['username'])
        isLoggedIn = True
        if(user_obj.weight.isnumeric()):
            weight = user_obj.weight
        if(user_obj.height.isnumeric()):
            height = user_obj.height

    return render(request , 'bmi.html' , {'isLoggedIn' : isLoggedIn , 'username' : username , 'weight' : weight , 'height': height })

def home(request):
    global username
    global isLoggedIn 
    if request.session.has_key('username'):
        #print(request.session['username'])
        isLoggedIn = True
        username = setUserName(request.session['username'])
    return render(request , 'index.html' , {'isLoggedIn':isLoggedIn,'username':username})


def recipe(request, id):
    print(id)
    return render(request, 'recipe.html', {'username':username})
