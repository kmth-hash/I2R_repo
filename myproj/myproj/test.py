import pandas as pd
import sys , os
from .models import Users ,Recipes , Recipe_Ingredients, Category, Ingredients

def store_users():
    files_DIR = os.getcwd()+"\\myproj\\files"
    try:
        file1 = pd.read_csv(files_DIR+"\\myproj_users.csv")
    except:
        pass

def store_categories():
    files_DIR = os.getcwd()+"\\myproj\\files"
    file1 = open(files_DIR+"\\myproj_category.csv" , "r")
    l1 = file1.readlines()
    f1 = pd.DataFrame(pd.read_csv(files_DIR+"\\myproj_category.csv"))
    
    for index, row in f1.iterrows():
        #print(row['Category_Id'] ,row['Category_Name'])
        obj = Category(Category_Id = row['Category_Id'] , 
                       Category_Name = row['Category_Name'])
        print(obj)
        obj.save()


def store_recipes():
    files_DIR = os.getcwd()+"\\myproj\\files"
    file1 = open(files_DIR+"\\myproj_recipes.csv" , "r")
    f1 = pd.DataFrame(pd.read_csv(files_DIR+"\\myproj_recipes.csv"))
    
    for index, row in f1.iterrows():
        #print(row['Recipe_Id'] ,index+1)
        
        obj = Recipes(  Receipe_Id = index+1 , 
                        Category_Id_id = row['Category_Id_id'] ,
                        Name = row['Name'] ,
                        Fats = row['Fats'] ,
                        Calories= row['Calories'] ,
                        Quantity = row['Quantity'] ,
                        Proteins=row['Proteins'] ,
                        Carbohydrates=row['Carbohydrates'] ,
                        Receipe_Image = row['Receipe_Image'] ,
                        Description = row['Description'] ,
                        procedure = row['procedure'], 
                        Ingredients = row['ingredients']
                        )
        print(obj)
        obj.save()
    
def store_ingredients():
    files_DIR = os.getcwd()+"\\myproj\\files"
    file1 = open(files_DIR+"\\myproj_ingredients.csv" , "r")
    l1 = file1.readlines()
    f1 = pd.DataFrame(pd.read_csv(files_DIR+"\\myproj_ingredients.csv"))
    
    for index, row in f1.iterrows():
        #print(row['Category_Id'] ,row['Category_Name'])
        obj = Ingredients(Ingredient_id=  row['Ingredient_id'] , 
                       name = row['name'] ,
                       Ingredient_image = row['Ingredient_image'] ,
                       Type = row['Type']
                       )
        print(obj)
        obj.save()

def store_rec_ing():
    files_DIR = os.getcwd()+"\\myproj\\files"
    file1 = open(files_DIR+"\\myproj_recipe_ingredients.csv" , "r")
    l1 = file1.readlines()
    f1 = pd.DataFrame(pd.read_csv(files_DIR+"\\myproj_recipe_ingredients.csv"))
    
    for index, row in f1.iterrows():
        #print(row['Category_Id'] ,row['Category_Name'])
        obj = Recipe_Ingredients(Receipe_Ingredient_Id = row['Receipe_Ingredient_Id'] , 
                       Ingredient_Id_id = row['Ingredient_Id_id'],
                       Receipe_Id_id = row['Receipe_Id_id'])
        print(obj)
        obj.save()

def storeDBfromCSV():
    store_categories()
    store_ingredients()
    store_recipes()    
    store_rec_ing()

