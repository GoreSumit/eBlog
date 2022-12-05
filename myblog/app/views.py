from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from .forms import UserForm,UserLogin,PostForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Post


# Create your views here
def home(request):
    user_posts = Post.objects.all()
    return render(request,'home.html',{'posts':user_posts})

def sign_up(request):
    if request.method=="POST":
        fm=UserForm(request.POST)
        if fm.is_valid():
            fm.save()
            fm=UserForm()
            messages.success(request,"User Created Successfully, Please Login")
            return HttpResponseRedirect('/login/')
    else:
        fm=UserForm()
        return render(request,'signup.html',{'form':fm})

def user_login(request):
    if request.method=='POST':
        fm = UserLogin(request=request,data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            print(uname,upass)
            user = authenticate(username=uname,password=upass)
            if user is not None:
                login(request,user)
                messages.success(request,"Login Successful")
                return HttpResponseRedirect('/profile/')
        else:
            messages.warning(request,"User does not exist or wrong credentials")
            return render(request,'login.html',{'form':fm})
    else:
        fm=UserLogin()
        return render(request,'login.html',{'form':fm})
    
    
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

def user_profile(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            fm = PostForm(request.POST)
            posts=Post.objects.filter(user_id=request.user.id)
            if fm.is_valid():
                profile = fm.save(commit=False)
                profile.user = request.user
                profile.save()
                messages.success(request,"Post Updated")
                return render(request,'profile.html',{'posts':posts,'modalform':fm})
        else:
            fm = PostForm()
            posts=Post.objects.filter(user_id=request.user.id)
            return render(request,'profile.html',{'posts':posts,'modalform':fm})
    else:
        return HttpResponseRedirect('/login/')
    
    
    
def add_post(request):
    if request.user.is_authenticated:    
        if request.method=='POST':
            fm = PostForm(request.POST)
            if fm.is_valid():
                title = fm.cleaned_data['title']
                desc = fm.cleaned_data['desc']
                profile = fm.save(commit=False)
                profile.user = request.user
                profile.save()
                messages.success(request,"Post Updated")    
            return render(request,'profile.html',{'modalform':fm})
        else:
            fm=PostForm()    
            return render(request,'profile.html',{'modalform':fm})
    else:
        return HttpResponseRedirect('/login/') 

def updatedata(request,id):
    if request.user.is_authenticated:
        userid = request.user.id
        get_id=Post.objects.get(pk=id).user_id
        if userid == get_id:
            if request.method=="POST":
                dat=Post.objects.get(pk=id)
                fm = PostForm(request.POST,instance=dat)
                if fm.is_valid():
                    fm.save()
                    messages.success(request,"Post edit Successful")
                    return HttpResponseRedirect('/profile/')
            else:
                dat=Post.objects.get(pk=id)
                fm=PostForm(instance=dat)
                return render(request,'edit.html',{'form':fm})
            
        else:
            messages.warning(request,"You do not have permission for this task")
            return HttpResponseRedirect('/profile/')
    else:
        return HttpResponseRedirect('/login/')
  
def deletedata(request,id):
    if request.user.is_authenticated:
        userid = request.user.id
        get_id=Post.objects.get(pk=id).user_id
        if userid == get_id:
            if request.method=="POST":
                dat=Post.objects.get(pk=id)
                dat.delete()
                return HttpResponseRedirect('/profile/')
        else:
            messages.warning(request,"You do not have permission for this task")
            return HttpResponseRedirect('/profile/')
    else:
        return HttpResponseRedirect('/login/')
'''
def updatedata(request,id):
    if request.user.is_authenticated:   
        if request.method=="POST":
            dat=Post.objects.get(pk=id)
            fm = PostForm(request.POST,instance=dat)
            if fm.is_valid():
                fm.save()
                messages.success(request,"Post edit Successful")
                return HttpResponseRedirect('/profile/')
        else:
            dat=Post.objects.get(pk=id)
            fm=PostForm(instance=dat)
            return render(request,'edit.html',{'form':fm})
    else:
        return HttpResponseRedirect('/login/')

'''


'''
    if user is not None:
                login(request,user)
                messages.success(request,"Login Successful")
                return HttpResponseRedirect('/profile/')
            else:
                messages.warning(request,"User does not exist")
                return HttpResponseRedirect('/signup/')
'''