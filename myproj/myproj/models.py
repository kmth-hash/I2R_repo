from django.db import models

class Users(models.Model):
    username = models.TextField()
    password = models.TimeField()
    height = models.TextField()
    weight = models.TextField()
    role = models.TextField()

class Ingredients(models.Model):
    Ingredient_id = models.IntegerField(primary_key=True)
    name = models.TextField()
    Ingredient_image = models.ImageField(upload_to = 'images/Ingredients/')
    Type = models.TextField()

class Recipe_Ingredients(models.Model):
    Receipe_Ingredient_Id = models.IntegerField(primary_key=True)
    Receipe_Id = models.ForeignKey("Recipes",on_delete=models.SET_NULL,null=True)
    Ingredient_Id = models.ForeignKey("Ingredients",on_delete=models.SET_NULL,null=True)

class Recipes(models.Model):
    Receipe_Id = models.IntegerField(primary_key=True)
    Category_Id = models.ForeignKey("Category",on_delete=models.SET_NULL,null=True)
    Name = models.TextField()
    Fats = models.TextField()
    Calories = models.TextField()
    Quantity = models.TextField()
    Proteins = models.TextField()
    Carbohydrates = models.TextField()
    Receipe_Image = models.ImageField(upload_to = 'images/Receipe')

class Category(models.Model):
    Category_Id = models.IntegerField(primary_key=True)
    Category_Name = models.TextField()