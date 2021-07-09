import os
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('signup/' , views.signup) , 
    path('login/' , views.login) ,
    path('home/' , views.home) ,
    path('profile/' , views.profile) ,
    path('logout/' , views.logout) ,
    # path('splash/' , views.splash) , 
    path('search/recipes/recipe/<str:id>/', views.recipe) ,
    path('search/recipes/' , views.recipes) ,
    path('addRecipe/' , views.addRecipe) , 
    path('add/', views.addNewRecipe),
    path('' , views.firstcall) , 
    path('signup/profile/' , views.signupprofile) , 
    path('search/' , views.mainpage) , 
    path('callme/',views.recipes),
    path('adminpanel/',views.admin)
    
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)