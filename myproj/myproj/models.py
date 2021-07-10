from django.db import models

class Users(models.Model):
    username = models.TextField()
    email = models.TextField(default="")
    password = models.TextField()
    role = models.TextField()

    def __str__(self):
        return "Name : "+self.username
    
class User_Details(models.Model):
    User_Id = models.ForeignKey("Users",on_delete=models.CASCADE,null=True)
    height = models.TextField()
    weight = models.TextField()
    age = models.TextField()
    gender = models.TextField()
    Calories = models.TextField()

    def __str__(self):
        return "Name : "+self.User_Id

class Receipe_Tracker(models.Model):
    User_Id = models.ForeignKey("Users",on_delete=models.SET_NULL,null=True)
    Receipe_Id = models.ForeignKey("Recipes",on_delete=models.SET_NULL,null=True)
    Day = models.TextField()
    qty = models.IntegerField()
    def __str__(self):
        return "happy"

class Ingredients(models.Model):
    Ingredient_id = models.IntegerField(primary_key=True  )
    name = models.TextField()
    Ingredient_image = models.ImageField(upload_to = 'images/Ingredients/')
    Type = models.TextField()

    def __str__(self):
        return "Item name : "+self.name

class Recipes(models.Model):
    Receipe_Id = models.IntegerField(primary_key=True)
    Category_Id = models.ForeignKey("Category",on_delete=models.CASCADE,null=True)
    Name = models.TextField()
    Fats = models.TextField()
    Calories = models.TextField()
    Quantity = models.TextField()
    Proteins = models.TextField()
    Carbohydrates = models.TextField()
    Receipe_Image = models.ImageField(upload_to = 'images/Receipe')
    Description = models.TextField(default="")
    procedure = models.TextField(default="")
    Ingredients = models.TextField(default="")

    def __str__(self):
        return "Recipe name : "+self.Name
class Recipe_Ingredients(models.Model):
    Receipe_Ingredient_Id = models.IntegerField(primary_key=True)
    Receipe_Id = models.ForeignKey("Recipes",on_delete=models.CASCADE,null=True)
    Ingredient_Id = models.ForeignKey("Ingredients",on_delete=models.SET_NULL,null=True)
    Qty = models.DecimalField(decimal_places=2 ,max_digits=10 , default= 0)
        
    def __str__(self):
        return "Too many numbers. Math.No No."

class Category(models.Model):
    Category_Id = models.IntegerField(primary_key=True)
    Category_Name = models.TextField()

    def __str__(self):
        return "Category : "+self.Category_Name

class recipe_liked_table(models.Model):
    Receipe_Id = models.ForeignKey("Recipes",on_delete=models.CASCADE,null=True)
    User_Id = models.ForeignKey("Users",on_delete=models.CASCADE,null=True)
        
class recipe_like_count(models.Model):
    Receipe_Id = models.ForeignKey("Recipes",on_delete=models.CASCADE,null=True)
    likes = models.IntegerField()
