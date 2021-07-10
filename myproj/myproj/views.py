from django.shortcuts import render , redirect
from .models import *
from django.contrib import messages
from django.http import HttpResponse , JsonResponse
from .test import storeDBfromCSV
from .add_ons import *
import datetime 
from json import *
import json
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
predicted_items=[]
user_id = None
name=""


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
    if not request.session.has_key('username'):
        return redirect('/login')
    global isLoggedIn
    user_id = request.session['uid']
    email = request.session['email']
    username = request.session['username']
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
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM myproj_recipes as t1,myproj_receipe_tracker as t2 WHERE t1."Receipe_Id"=t2."Receipe_Id_id" AND t2."User_Id_id"=%s ORDER BY t2."Day"',[user_id])
            row = cursor.fetchall()
            user_recipe_list = list()
            for i in row:
                user_recipe_list.append(i)
                print(i[16])
    return render(request,'profile.html',{'isLoggedIn':isLoggedIn,'username':username,'data':item,'mail':email,'uid':user_id,'user_receipe_list':user_recipe_list})
def firstcall(request):
    print("here inside first")
    if request.session.has_key('username'):
        uid=request.session['uid']
        with connection.cursor() as cursor:
                cursor.execute('SELECT "Calories" FROM myproj_user_details WHERE "User_Id_id"=%s',[uid])
                row = cursor.fetchone()
                calories = row[0]
                request.session['remaining_calories_perday']=calories
                cursor.close()
        request.session['imagestopreview']=[]
        request.session['predicted_items']=[]
        request.session['recipe_array']=[]
    return redirect('/home')
def predict(iurl,predicted_items,request):
    toexecute = 'python yolov5/detect.py --weights probably_the_last_one.pt --img 640 --conf 0.1 --source '
    jh=[]
    toexecute+=iurl
    gh=os.system(toexecute)
    with open('predictions.txt','r') as f:
        for line in f:
            jh.append(line.strip())
            if line.strip().title() not in predicted_items:
                predicted_items.append(str(line.strip()).title())
    request.session['predicted_items']=predicted_items
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
    uid=request.session['uid']
    if not request.session.has_key('username'):
        return redirect('/login')
    if request.method == "POST":
        recipes_array=request.session['recipe_array']
        if not request.POST.get('cheatday', None) == None:
            print("its a cheatday")
        else:
            id = request.POST['continue_button']
            qty = request.POST['num_qty']
            updateTracker(uid,recipes_array[int(id)]['recipe_id'],qty)
        request.session['recipe_array'] = recipes_array[int(id)]
        # return redirect('/search/recipes')
        return redirect('/search/recipes/recipe/'+id)
    else:
        predicted_items=request.session['predicted_items']
    username=request.session['username']
    a=[]
    remaining_calories=[]
    recipes_array=[]
    recipe_string = ', '.join(map(str, predicted_items))
    consumed_calories = getDailyCal(uid)
    calories = request.session['remaining_calories_perday']
    calories = int(calories) - int(consumed_calories)
    for i in return_recipes(predicted_items):
        # recipes_array.append(i)
        if i[1]>20.0:
            with connection.cursor() as cursor:
                cursor.execute('SELECT "Category_Name" from myproj_category where "Category_Id"=%s',[i[0][11]])
                row = cursor.fetchone()
            connection.close()
            recipe_details = {
            'recipe_id':i[0][0],
            'name':i[0][1],
            'fats':i[0][2],
            'calories':i[0][3],
            'quantity':i[0][4],
            'proteins':i[0][5],
            'carbohydrates':i[0][6],
            'imageURL':str(i[0][7]),
            'description':i[0][8],
            'procedure':i[0][9],
            'ingredients':i[0][10],
            'category':row[0],
            'remaining_calories':int(calories)//int(i[0][3])
            
            }
            print(i[0][10])
            recipes_array.append(recipe_details)
        else:
            pass
        
    # 'recipe_id':recipe_id,
    #                 'name':list(j)[1],
    #                 'fats':list(j)[2],
    #                 'calories':list(j)[3],
    #                 'quantity':list(j)[4],
    #                 'proteins':list(j)[5],
    #                 'carbohydrates':list(j)[6],
    #                 'imageURL':list(j)[7],
    #                 'description':list(j)[8],
    #                 'procedure':list(j)[9],
    #                 'ingredients':list(j)[10],
    #                 'remaining_calories':int(calories)//int(list(j)[3])
    request.session['recipe_array'] = recipes_array
    return render(request , 'recipes.html' , {'recipe_data':recipes_array,'predicted_items':recipe_string,'username':username,'calories':calories})

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
                role = res.role
                if role == "admin":
                    return redirect('/adminpanel')
                isLoggedIn = True
                request.session['uid'] = user_obj.id
                request.session['username'] = user_obj.username
                request.session['email'] = user_obj.email
                request.session['imagestopreview']=[]
                request.session['predicted_items']=[]
                request.session['recipe_array']=[]

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
                return redirect("/home" , isLoggedIn = True , username = user_obj.username)  
                        
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
        del request.session['imagestopreview']
        del request.session['predicted_items']
        del request.session['remaining_calories_perday']
        del request.session['recipe_array']
        isLoggedIn = False
        username = ''
        imagesToPreview=[]
        datajson=[]
        messages.success(request , 'Successfully Logged out')
    except:
        messages.error(request , 'Error while logging out')
    return redirect('/home')

def mainpage(request):
    if not request.session.has_key('username'):
        return redirect('/login')
    imagesToPreview=request.session['imagestopreview']
    predicted_items = request.session['predicted_items']
    print(predicted_items)
    username = request.session['username']
    if request.method == "POST" and request.POST.get("form_close") == 'form_close':
        imagesToPreview=request.session['imagestopreview']
        predicted_items=request.session['predicted_items']
        del predicted_items[int(request.POST['close_button'])-1]
        del imagesToPreview[int(request.POST['close_button'])-1]
        request.session['imagestopreview']=imagesToPreview
        request.session['predicted_items']=predicted_items
        return redirect('/search')
    
    elif request.method == 'POST' and request.POST.get("recipe") == 'recipe':
        return redirect('/search/recipes')

    elif request.method == 'POST' and request.POST.get("predciton") == 'predciton':
        if request.POST['Name']:
            image_text = request.POST['Name']
            uploaded_file_url = '/media/veg/'+str(image_text).lower()+'.jpg'
            imageAndName = {
                'imageURL':uploaded_file_url,
                'name':image_text
            }
            print("bye")
            print(predicted_items)
            if str(image_text).title() not in predicted_items:
                print("hello")
                predicted_items.append(str(image_text).title())
                imagesToPreview.append(imageAndName)
                request.session['predicted_items']=predicted_items
            request.session['imagestopreview']=imagesToPreview
            return redirect('/search')
        else:
            doc = request.FILES
            doc_name = doc['image']
            fs = FileSystemStorage()
            filename = fs.save(doc_name.name, doc_name)
            uploaded_file_url = fs.url(filename)
            predictedImage = predict(str(uploaded_file_url)[1:],predicted_items,request)
            listToStr = ', '.join(map(str, predictedImage))
            imageAndName = {
                'imageURL':uploaded_file_url,
                'name':listToStr
            }
            imagesToPreview.append(imageAndName)
            # request.session['imagestopreview']=imagesToPreview

    return render(request , 'mainpage.html' , {'len':len(imagesToPreview),'imagesToPreview':imagesToPreview , 'isLoggedIn' : isLoggedIn , 'username' : username })

def addRecipe(request):
    storeDBfromCSV()
    return render(request , 'addRecipe.html' , {}) 

# def bmi(request):
#     if not request.session.has_key('username'):
#         return redirect('/login')
#     global isLoggedIn
#     username = ''
#     weight = 0
#     height = 0
#     if request.session.has_key('username'):
#         username = setUserName(request.session['username'])
#         user_obj = Users.objects.get( username = request.session['username'])
#         isLoggedIn = True
#         if(user_obj.weight.isnumeric()):
#             weight = user_obj.weight
#         if(user_obj.height.isnumeric()):
#             height = user_obj.height

#     return render(request , 'bmi.html' , {'isLoggedIn' : isLoggedIn , 'username' : username , 'weight' : weight , 'height': height })

def home(request):
    global username
    global isLoggedIn
    recommendations=[]
    with connection.cursor() as cursor:
                cursor.execute('SELECT * from myproj_recipes as t1,myproj_recipe_like_count as t2 WHERE t1."Receipe_Id"=t2."Receipe_Id_id" AND t2.likes>=1 ORDER BY t2."likes" DESC LIMIT 5')
                row = cursor.fetchall()
                if len(row)!=0:
                    recommendations.append(row)
    connection.close()
    if request.session.has_key('username'):
        #print(request.session['username'])
        isLoggedIn = True
        username = setUserName(request.session['username'])
    return render(request , 'index.html' , {'isLoggedIn':isLoggedIn,'username':username,'recommendation':recommendations})

def addNewRecipe(request):
    if request.session.has_key('username'):
        user = Users.objects.get(username = request.session['username'] )
        if user.role.lower() == 'admin':
            return render(request, 'add.html', {'isLoggedIn' : True , 'username' : user.username } )
        else:
            return redirect('/')

    else:
        return redirect('/home')


def recipe(request, id):
    tolist=request.session['recipe_array']
    recipe_id=tolist['recipe_id']
    uid=request.session['uid']
    if request.method == "POST" and request.POST.get("form_type") == 'present':
        with connection.cursor() as cursor:
                cursor.execute('DELETE FROM myproj_recipe_liked_table WHERE "Receipe_Id_id"=%s and "User_Id_id"=%s',[recipe_id,uid])
                cursor.execute('UPDATE myproj_recipe_like_count SET likes = likes - 1 WHERE "Receipe_Id_id"=%s',[recipe_id])
        connection.close()
        return redirect('/search/recipes/recipe/'+id)
    elif request.method == "POST" and request.POST.get("form_type") == 'notpresent':
        with connection.cursor() as cursor:
                cursor.execute('INSERT INTO myproj_recipe_liked_table VALUES(%s,%s)',[recipe_id,uid])
                cursor.execute('UPDATE myproj_recipe_like_count SET likes = likes + 1 WHERE "Receipe_Id_id"=%s',[recipe_id])
        connection.close()
        return redirect('/search/recipes/recipe/'+id)
    else:
        print("reached inside else")
        with connection.cursor() as cursor:
                cursor.execute('SELECT "likes" from myproj_recipe_like_count WHERE "Receipe_Id_id"=%s',[recipe_id])
                row = cursor.fetchone()
                likes=row[0]
        connection.close()
        with connection.cursor() as cursor:
                cursor.execute('SELECT * from myproj_recipe_liked_table WHERE "Receipe_Id_id"=%s and "User_Id_id"=%s',[recipe_id,uid])
                row = cursor.fetchone()
                print(row)
                if str(row)=="None":
                    present = False
                else:
                    present = True
        connection.close()
    return render(request, 'recipe.html', {'username':username,'tolist':tolist,'likes':likes,'present':present})

def signupprofile(request):
    global user_id,name
    print("reached")
    if request.method == 'POST':
        height = request.POST['height']
        weight = request.POST['weight']
        age = request.POST['age']
        gender = request.POST['gender']
        if gender == 'male':
            BMR = int((10*float(weight)) + (6.25*float(height)) - (5*float(age)) + 5)
        else:
            BMR = int((10*float(weight)) + (6.25*float(height)) - (5*float(age)) - 161)
        user_details = User_Details(User_Id_id=user_id, height=height , weight = weight , age=age, gender=gender,Calories=BMR )
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
        print(user_list)
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

def updateTracker(userID,recipeID,qty):
    user = Users.objects.get(id = userID)
    recipeObj = Recipes.objects.get(Receipe_Id=recipeID)
    current_date = datetime.date.today()
    obj = Receipe_Tracker(User_Id=user, Receipe_Id=recipeObj,Day=current_date,qty=qty)
    obj.save()
    print('Tracker Updated for User : ',user.username)

        
def record(request,id):
    if not request.session.has_key('username'):
        return redirect('/login')
    global isLoggedIn

    user = Users.objects.get(id = id)
    userinfo = User_Details.objects.get(User_Id=user)
    
    print(user)
    data = getChartData(id)
    weeklyCaldata  = weeklyCalories(id)
    todayCal = getDailyCal(id)
    print(isLoggedIn)
    print(weeklyCaldata , todayCal)
    labels = json.dumps(data['labels']) 
    datasets = json.dumps(data['datasets'][0]['data'])
    #updateTracker(user.id,1,False)
    
    return render(request, "records.html" , {'labels' : labels ,
                                            "datasets":datasets, 'isLoggedIn' : isLoggedIn , 
                                            'username' : user.username, 'user' : user , 
                                            'userinfo' : userinfo , 'weeklyCal' : weeklyCaldata , 'dailyCal' : todayCal })
