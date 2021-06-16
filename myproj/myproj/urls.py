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
    path('recipes/' , views.recipes) ,
    path('addRecipe/' , views.addRecipe) , 
    path('' , views.mainpage) , 
    path('callme/',views.recipes)
    
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)