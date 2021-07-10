from django.shortcuts import render , redirect
from .models import Ingredients, Recipes , Category , Recipe_Ingredients , Users, User_Details,Receipe_Tracker
from django.contrib import messages
from django.http import HttpResponse , JsonResponse
from .test import storeDBfromCSV
from .add_ons import *
import datetime 
import json

from json import loads,dumps
from django.core.files.storage import FileSystemStorage
import os

from django.db import connection
import numpy as np

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

procedure=[]
predcited_items=[]
<<<<<<< HEAD
user_id = None
=======

user_id=""
>>>>>>> b73b3b3e0715d8d75568b6eec8c6fb7ebb92b70d
name=""
# from pathlib import Path
# fd=exec(Path("yolov5/detect.py").read_text())
# print(fd)
# print(gh)
def admin(request):
    return render(request,'adminpanel.html')
def item_return(userid):
    with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM myproj_user_details WHERE "User_Id_id"=%s',[userid])
            row = cursor.fetchall()
            item = []
            for j in row:
                item.append(list(j))
                # print(j)
    connection.close()
    return item
def profile(request):
    global isLoggedIn
    user_id = request.session['uid']
    email = request.session['email']
    username = setUserName(request.session['username'])
    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']
        height = request.POST['height']
        weight = request.POST['weight']
        with connection.cursor() as cursor:
            cursor.execute('UPDATE myproj_users SET "username"=%s WHERE "id"=%s',[name,user_id])
            cursor.execute('UPDATE myproj_user_details SET "height"=%s,"weight"=%s,"age"=%s WHERE "User_Id_id"=%s',[height,weight,age,user_id])
        connection.close()
        request.session['username'] = name
        messages.success(request , 'Profile Updated Successfully!')
        return redirect('/profile')
    else:
        item=item_return(user_id)
    return render(request,'profile.html',{'isLoggedIn':isLoggedIn,'username':username,'data':item,'mail':email})
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
    global isLoggedIn,user_id,name  
    if request.method=='POST' :
        name = request.POST['first_name']+" "+request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['conf_password']

        if password==confirm_password:
            new_user = Users(username= name , password = password , role = "user", email=email )
            new_user.save()
            request.session['username'] = name
            request.session['email'] = email

            isLoggedIn = True
            with connection.cursor() as cursor:
                cursor.execute('SELECT "id" FROM myproj_users WHERE "username"=%s and "password"=%s',[name,password])
                row = cursor.fetchone()
                user_id = row[0]
                request.session['uid'] = user_id
                cursor.close()
            return redirect('/signup/profile')
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
                print(list(j))
                recipe_details = {
                    'id' :list(j)[0],
                    'name':list(j)[1],
                    'fats':list(j)[2],
                    'calories':list(j)[3],
                    'quantity':list(j)[4],
                    'proteins':list(j)[5],
                    'carbohydrates':list(j)[6],
                    'imageURL':list(j)[7],
                    'description':list(j)[8],
                    'procedure':list(j)[9],
                    'ingredients':list(j)[10]
                }
                recipes_array.append(recipe_details)
        connection.close()
    recipe_json = dumps(recipes_array)
    global isLoggedIn
    user = request.session['username']

    return render(request , 'recipes.html' , {'recipe_data':recipes_array,'predcited_items':recipe_string,'username':user,'isLoggedIn': isLoggedIn })

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
                print(user_obj.role)
                role = user_obj.role
                if role == "admin":
                    return redirect("/adminpanel")
                isLoggedIn = True
                request.session['uid'] = user_obj.id
                request.session['username'] = user_obj.username
                request.session['email'] = user_obj.email
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
        del request.session['uid']
        del request.session['email']
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
            uploaded_file_url = '/assets/img/veg/'+str(image_text).lower()+'.jpg'
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
    storeDBfromCSV()
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

def addNewRecipe(request):
    if request.session.has_key('username'):
        user = Users.objects.get(username = request.session['username'] )
        if user.role.lower() == 'admin':
            return render(request, 'add.html', {'isLoggedIn' : True , 'username' : user.username } )
        else:
            return redirect('/')

    else:
        return redirect('/')


def recipe(request, id):
    global isLoggedIn
    recipe = Recipes.objects.get(Receipe_Id=id)
    ing_list = []
    temp = Recipe_Ingredients.objects.filter(Receipe_Id=id)
    for i in temp:
        ing_list.append(Ingredients.objects.get(Ingredient_id=i.Ingredient_Id_id).name)
    print(ing_list)
    print(recipe.Description, recipe.Fats)
    return render(request, 'recipe.html', {'isLoggedIn': isLoggedIn, 'username':username , 'ing_list': ing_list, 'recipe' : recipe })

def signupprofile(request):
    global user_id,name
    print("reached")
    if request.method == 'POST':
        height = request.POST['height']
        weight = request.POST['weight']
        age = request.POST['age']
        gender = request.POST['gender']
        user_details = User_Details(User_Id_id=user_id, height=height , weight = weight , age=age, gender=gender,Calories="2000" )
        user_details.save()
        messages.success(request  , " Signup successful.")
        return redirect('/')
    return render(request, "signupprofile.html",{'username':name})


def users():
    with connection.cursor() as cursor:
        cursor.execute('SELECT  t1.id,t1.username,t1.email,t2.height,t2.weight,t2.age,t2.gender from myproj_users as t1,myproj_user_details as t2 WHERE t1.id = t2."User_Id_id" ' )
        row = cursor.fetchall()
        user_list = list()
        for values in row:
            user_list.append(list(values)) 
    connection.close()
    return user_list


def receipe_returned():
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM myproj_recipes' )
        row = cursor.fetchall()
        recipe_list = list()
        for values in row:
            recipe_list.append(list(values)) 
    connection.close()
    return recipe_list



def admin(request):
    if request.method == "POST" and request.POST.get("form_type") == 'formOne':
        id_return = request.POST['delete_button']
        with connection.cursor() as cursor:
            cursor.execute('DELETE from myproj_user_details where "User_Id_id"=%s',[id_return])
            cursor.execute('DELETE from myproj_users where "id"=%s',[id_return])
        connection.close()
        user_list = users()
        #print(user_list)
        return redirect("/adminpanel")
    elif  request.method == "POST" and request.POST.get("form_type") == 'formTwo':
        id_return = request.POST['recipe_delete_button']
        with connection.cursor() as cursor:
            cursor.execute('DELETE from myproj_recipe_ingredients where "Receipe_Id_id"=%s',[id_return])
            cursor.execute('DELETE from myproj_recipes where "Receipe_Id"=%s',[id_return])
        connection.close()
        receipe_list = receipe_returned()
        return redirect("/adminpanel")

    elif request.method == "POST" and request.POST.get("form_type") == 'formThree':
        name = request.POST['new_recipe']
        quantity = request.POST['new_quantity']
        description = request.POST['new_desc']
        calories = request.POST['new_calories']
        proteins = request.POST['new_proteins']
        fats = request.POST['new_fats']
        carbohydrates = request.POST['new_carbo']
        ingredients = request.POST['new_ing']
        procedure = request.POST['new_procedure']
        category = request.POST['new_category']
        ing_list = list(ingredients.split(','))
        ing_list_tags = list(ingredients.split(','))
        for i in range(len(ing_list)):
            ing_list_tags[i] = "&#9830"+ing_list[i]+"<br>"
        
        recipe_ingredient_to_add = " ".join(ing_list_tags)

        image_to_add = "assests/img/rec/"+name+".png"
        category_obj = Category.objects.get(Category_Name=category)
        category_id = category_obj.Category_Id
        max_recp_obj = Recipes.objects.last()
        max_key = max_recp_obj.Receipe_Id

        procedure_list = list(procedure.split(','))
        print(procedure_list)
        loop_count = 1
        for j in range(len(procedure_list)):
            procedure_list[j] = "<h2>Step"+str(loop_count)+"</h2> "+procedure_list[j]+"<br>"
            loop_count += 1
        procedure_to_add = " ".join(procedure_list)



        new_recipe = Recipes(
                        Receipe_Id = max_key + 1,
                        Category_Id_id = category_id ,
                        Name = name ,
                        Fats = fats ,
                        Calories= calories ,
                        Quantity = quantity ,
                        Proteins= proteins ,
                        Carbohydrates=carbohydrates ,
                        Receipe_Image = image_to_add ,
                        Description = description ,
                        procedure = procedure_to_add, 
                        Ingredients = recipe_ingredient_to_add)
        new_recipe.save()
        messages.success(request  , " Added successfully.")
       
        ingredient_id_list = list()
        for names in ing_list:
            ingredient_id = Ingredients.objects.get(name=names).Ingredient_id
            ingredient_id_list.append(ingredient_id)
        print(ingredient_id_list)
        max_recp_ing_obj = Recipe_Ingredients.objects.last()
        max_key_ing = max_recp_ing_obj.Receipe_Ingredient_Id
        count = 1
        for id in ingredient_id_list:
            max_key_ing += count
            new_ing_obj = Recipe_Ingredients(Receipe_Ingredient_Id=max_key_ing,Qty=0.00,Ingredient_Id_id=id,Receipe_Id_id=max_key+1)
            new_ing_obj.save()
            count +=1
        

        return redirect("/adminpanel")

    else:
        user_list = users()
        receipe_list = receipe_returned()
        #print(receipe_list)
    
    
    return render(request,"adminpanel.html", {'user_list':user_list,'recipe_list':receipe_list})

def updateTracker(userID,recipeID,cheatDay):
    user = Users.objects.get(id = userID)
    recipeObj = Recipes.objects.get(Receipe_Id=recipeID)
    current_date = datetime.date.today()
    if not cheatDay :
        obj = Receipe_Tracker(User_Id=user, Receipe_Id=recipeObj,Day=current_date)
        obj.save()
        print('Tracker Updated for User : ',user.username)

        
def record(request,id):
    global isLoggedIn

    user = Users.objects.get(id = id)
    userinfo = User_Details.objects.get(User_Id=user)
    
    print(user)
    data = getChartData(id)
    weeklyCaldata  = weeklyCalories(id)
    todayCal = getDailyCal(id)
    
    print(weeklyCaldata , todayCal)
    labels = json.dumps(data['labels']) 
    datasets = json.dumps(data['datasets'][0]['data'])
    #updateTracker(user.id,1,False)
    
    return render(request, "records.html" , {'labels' : labels ,
                                            "datasets":datasets, 'isLoggedIn' : isLoggedIn , 
                                            'username' : user.username, 'user' : user , 
                                            'userinfo' : userinfo , 'weeklyCal' : weeklyCaldata , 'dailyCal' : todayCal })
