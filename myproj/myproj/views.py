from django.shortcuts import render , redirect
from .models import Ingredients, Recipes , Category , Recipe_Ingredients , Users
from django.contrib import messages
from django.http import HttpResponse
from .test import storeDBfromCSV
from .add_ons import *

from json import loads,dumps
from django.core.files.storage import FileSystemStorage
from keras import preprocessing
import matplotlib.pyplot as plt
import numpy as np
from keras.models import load_model
from keras import backend as K

imagesToPreview = []
predictedNames = []
isLoggedIn = False


datajson = []
def predict(iurl):
    K.clear_session()
    model = load_model('vegetable_predict_3.h5')
    labels = ['Apple','Banana','Beetroot','Cauliflower','Corn','Onion','Orange','Potato','Tomato','Watermelon']
    test_image = preprocessing.image.load_img(iurl,target_size=(224,224))
    test_image = preprocessing.image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis = 0)
    result = model.predict(test_image)
    K.clear_session()
    result1 = result[0]
    for i in range(0,10):
        if result1[i] == 1.:
            break;
    prediction = labels[i]
    return prediction
def signup(request):    
    if request.method=='POST' :
        name = request.POST['first_name']+" "+request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['conf_password']

        if password==confirm_password:
            new_user = Users(username= name , password = password , height = "" , weight = "" , role = "user", email=email )
            new_user.save()
            request.session['username'] = name
            messages.success(request  , " Signup successful.")
            return redirect("/")
        else:
            messages.error(request  , " Password did not match.")
            return redirect("/signup")              
       

    return render(request , 'signup.html' , {})

def recipes(request):
    return render(request , 'recipes.html' , {})

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

def mainpage(request):
    username = ''
    global isLoggedIn 
    if request.session.has_key('username'):
        print(request.session['username'])
        isLoggedIn = True
        username = setUserName(request.session['username'])

    global imagesToPreview,datajson
    if request.POST:
        imagesToPreview = loads(request.POST['hiddeninput'])
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
    return_recipes(['egg' , 'onion' , 'butter' , 'salt', 'pepper'])
    return render(request , 'addRecipe.html' , {})
def bmi(request):
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


