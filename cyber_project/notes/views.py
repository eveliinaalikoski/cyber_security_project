from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def index(request):
    print("USER", request.user)
    return render(request, "notes/index.html", {"user": request.user})

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("USER", username, password)

        try:
            user = User.objects.create_user(
                username=username,
                password=password
            )
            print("USER", user)
            return redirect("/login")
        except:
            print("Something went wrong")
            return render(request, "notes/register.html")
            
    return render(request, "notes/register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        print("USER", username, password)
        
        user = authenticate(request, 
                            username=username, 
                            password=password)
        print("UU", user)

        if user is not None:
            login(request, user)
            return redirect("/")
        print("ONGELMA")

    return render(request, "notes/login.html")

def logout_view(request):
    logout(request)
    return redirect("/")
