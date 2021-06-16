
from .models import Ingredients , Recipe_Ingredients , Recipes 
from django.db.models.functions import Lower

def Ing_details(name):
    inst_name = " ".join( i.capitalize() for i in  name.split(" "))
    print(inst_name)
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
        return(res/len(other_rec_list)*100)



def return_recipes(curr_list = []):
    print(curr_list)
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
               
        rating_recipe[itr.Name] = compare_rec( my_ing , ing_list )
    rating_recipe = sorted(rating_recipe.items() , key=lambda x : x[1] , reverse= True)
    print(rating_recipe)

        
    
def setUserName(username):
    if len(username.split(' '))>1:
        return (username.split(' ')[0]).capitalize()
    else :
        return username.capitalize()            


    





