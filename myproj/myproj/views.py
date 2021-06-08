from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from json import dumps,loads

imagesToPreview=[]
datajson=[]
def signup(request):
    return render(request , 'signup.html' , {})

def login(request):
    return render(request , 'login.html' , {})

def mainpage(request):
    global imagesToPreview,datajson
    if request.POST:
        imagesToPreview = loads(request.POST['hiddeninput'])
        doc = request.FILES #returns a dict-like object
        doc_name = doc['image']
        fs = FileSystemStorage()
        filename = fs.save(doc_name.name, doc_name)
        uploaded_file_url = fs.url(filename)
        imagesToPreview.append(uploaded_file_url)
        datajson = dumps(imagesToPreview)
    return render(request , 'mainpage.html' , {'len':len(imagesToPreview),'imagesToPreview':imagesToPreview,'data':datajson})

def bmi(request):
    return render(request , 'bmi.html' , {})


