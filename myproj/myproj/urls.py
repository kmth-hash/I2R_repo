import os
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/' , views.signup) , 
    path('login/' , views.login) ,
    path('home/' , views.home) ,
    path('logout/' , views.logout) ,
    path('bmi/' , views.bmi) , 
    path('search/recipes/recipe/<int:id>/', views.recipe) ,
    path('search/recipes/' , views.recipes) ,
    path('search/' , views.mainpage) ,
    path('addRecipe/' , views.addRecipe) , 
    path('' , views.firstcall) ,      
    
    
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)