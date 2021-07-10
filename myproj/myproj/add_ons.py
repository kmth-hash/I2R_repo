
from .models import *
from django.db.models.functions import Lower
import datetime 


def Ing_details(name):
    inst_name = " ".join( i.capitalize() for i in  name.split(" "))
    ingredient = Ingredients.objects.get(name = inst_name)
    d = dict({
        "name" : ingredient.name ,
        "ID" : ingredient.Ingredient_id , 
        "image" : ingredient.Ingredient_image ,
        "type" : ingredient.Type
    })
    return d

def compare_rec(my_recipe , other_recipe):
    if len(other_recipe)==0 or len(my_recipe)==0:
        return 0
    else:
        my_recipe_list = []
        other_rec_list = []
        for rec in my_recipe:
            my_recipe_list.append(rec)
        
        for rec in other_recipe:
            other_rec_list.append(rec.name)

        res = 0
        
        for i in other_rec_list:
            if i in my_recipe_list:            
                res+=1
            else:
                pass
        print(res)
        if len(other_rec_list)==1:
            print(len(my_recipe_list))
            return res/len(my_recipe_list)*100
        else:
            print(len(other_rec_list))
            return(res/len(other_rec_list)*100)



def return_recipes(curr_list = []):
    my_list = []
    my_ing  =  []
    rating_recipe = {}
    i = 0
    ing_list = []
    for i in curr_list:
        my_list.append(Ing_details(i))
        inst_name = " ".join( itr.capitalize() for itr in  i.split(" "))
        my_ing.append(inst_name)
    

    all_rec = Recipes.objects.all()
   

    for itr in all_rec:
        ing_list = []
        all_ing = Recipe_Ingredients.objects.filter(Receipe_Id = itr.Receipe_Id)
        for i in all_ing:            
            ing_list.append(i.Ingredient_Id)
        print(itr.Receipe_Image)
        rating_recipe[itr.Receipe_Id,itr.Name,itr.Fats,itr.Calories,itr.Quantity,itr.Proteins,itr.Carbohydrates,itr.Receipe_Image,itr.Description,itr.procedure,itr.Ingredients,itr.Category_Id_id] = compare_rec( my_ing , ing_list )
    rating_recipe = sorted(rating_recipe.items() , key=lambda x : x[1] , reverse= True)
    return(rating_recipe)
        
    
def setUserName(username):
    if len(username.split(' '))>1:
        return (username.split(' ')[0]).capitalize()
    else :
        return username.capitalize()            


def getChartData(userID):
    user = Users.objects.get(id = userID)
    trackerData = []
    days = []
    labels = []
    for i in range(7):
        d = datetime.date.today() - datetime.timedelta(days = i)
        
        days.append(str(d))
    labels = days
    days.sort()
    print(days)
    for i in range(7):
        Kcal = Receipe_Tracker.objects.filter(User_Id=user, Day= days[i])
        dailyTotal = 0
        if len(Kcal)>0:
            for itr in Kcal:
                recipe = Recipes.objects.get(Receipe_Id= itr.Receipe_Id_id)
                #print(recipe)
                dailyTotal += float(recipe.Calories)
            
        trackerData.append(dailyTotal)
    
    data = dict()
    data['labels'] = days
    data['datasets'] = [{'data': trackerData,
								  "label": "Calorie Intake",
								  'borderColor': "#3e95cd",
								  'fill': False
								}]
    print(data)
    return data

def weeklyCalories(userId):
    user = Users.objects.get(id = userId)    
    weeklyCal = 0
    for i in range(7):
        d = datetime.date.today() - datetime.timedelta(days = i)        
        Kcal = Receipe_Tracker.objects.filter(User_Id=user, Day= str(d))
        
        if len(Kcal)>0:
            for itr in Kcal:
                recipe = Recipes.objects.get(Receipe_Id= itr.Receipe_Id_id)                
                weeklyCal += float(recipe.Calories)
            
    return weeklyCal


def getDailyCal(userId):
    user = Users.objects.get(id = userId)    
    calToday = 0
    
    d = datetime.date.today()     
    Kcal = Receipe_Tracker.objects.filter(User_Id=user, Day= str(d))
        
    if len(Kcal)>0:
        for itr in Kcal:
            recipe = Recipes.objects.get(Receipe_Id= itr.Receipe_Id_id)
            qtymulcal = float(recipe.Calories) * float(itr.qty)                
            calToday += qtymulcal
            
    return calToday

def getUserInfo(userId):
    u  = User_Details.objects.get(User_Id=userId)
    return u
