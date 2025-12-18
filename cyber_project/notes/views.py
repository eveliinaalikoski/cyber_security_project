from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import connection
from .models import Note

def index(request):
    notes = []
    if request.user.is_authenticated:
        notes = Note.objects.filter(owner=request.user)
    return render(request, "notes/index.html", {"user": request.user,
                                                "notes": notes})

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username and password:
            # A02 Cryptographic Failures
            try:
                user = User(username=username, password=password)
                user.save()
                return redirect("login")
            except Exception as e: # A04 Insecure Design
                return render(request,
                              "notes/register.html",
                              {"error": str(e)})

            # A02 Cryptographic Failures Fix
            # try:
            #     user = User.objects.create_user(
            #         username=username,
            #         password=password
            #     )
            #     return redirect("login")
            # except: # A04 Insecure Design Fix
            #     return render(request,
            #                   "notes/register.html",
            #                   {"error": "Register unsuccessful, try again"})

        else:
            return render(request, "notes/register.html", {"error": "Username and password are required"})
            
    return render(request, "notes/register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # A07 Indentification and Authentication Failures Fix
        # login_attempts = request.session.get("login_attempts", 0)
        # print("LOGIN", login_attempts)

        # if login_attempts >= 5:
        #     return render(request,
        #                   "notes/login.html",
        #                   {"error": "Too many login attempts, try again later"})

        if username and password:
            # A02 Cryptographic Failures & A07 Indentification and Authentication Failures
            try:
                user = User.objects.get(username=username)
                if user.password == password:
                    login(request, user)
                    return redirect("/")
                else:
                    # A04 Insecure Design
                    return render(request,
                                  "notes/login.html",
                                  {"error": f"Incorrect password for user {username}"})
                
            except Exception as e: # A04 Insecure Design
                return render(request, "notes/login.html", {"error": str(e)})

            # A02 Cryptographic Failures Fix
            # user = authenticate(request,
            #                     username=username,
            #                     password=password)

            # if user is not None:
            #     request.session["login_attempts"] = 0 # A07 Indentification and Authentication Failures Fix
            #     login(request, user)
            #     return redirect("/")
            # else:
            #     request.session["login_attempts"] = login_attempts + 1 # A07 Indentification and Authentication Failures Fix
            #     # A04 Insecure Design Fix
            #     return render(request,
            #                   "notes/login.html",
            #                   {"error": "Login unsuccessful, try again"})
        
        else:
            return render(request, "notes/login.html", {"error": "Username and password are required"})

    return render(request, "notes/login.html")

def logout_view(request):
    logout(request)
    return redirect("/")

def create_note(request):
    if request.method == "POST":
        content = request.POST.get("content")

        if content:
            Note.objects.create(owner = request.user,
                                content = content)
            return redirect("/")
    return render(request, "notes/create_note.html")

def note_view(request, noteid):
    note = Note.objects.get(pk=noteid)
    return render(request, "notes/note.html", {"note": note})
    
    # A01 Broken Access Control fix
    # try:
    #     note = Note.objects.get(pk=noteid, owner=request.user)
    #     return render(request, "notes/note.html", {"note": note})
    # except:
    #     return redirect("error")

def error_view(request):
    return render(request, "notes/error.html", {"error": "Restricted Access"})

def seach_notes(request):
    query = request.GET.get("query", "")
    notes = []

    if query and request.user.is_authenticated:
        cursor = connection.cursor()

        sql = """SELECT n.id, n.content, u.username 
                FROM notes_note n 
                JOIN auth_user u ON n.owner_id = u.id 
                WHERE n.owner_id='""" + str(request.user.id) + "' and n.content LIKE '%" + query + "%'"

        response = cursor.execute(sql).fetchall()

        # A03 Injection fix
        # sql = """SELECT n.id, n.content, u.username
        #         FROM notes_note n
        #         JOIN auth_user u ON n.owner_id = u.id
        #         WHERE n.owner_id = %(owner_id)s
        #         AND n.content LIKE %(query)s"""
        
        # response = cursor.execute(sql, {"owner_id": request.user.id, 
        #                                 "query": f"%{query}%"}).fetchall()

        for r in response:
            print("RESPONSE", r)
            notes.append({"id": r[0], "content": r[1], "owner": r[2]})

    return render(request, "notes/search_notes.html", {"query": query,
                                                       "notes": notes,
                                                       "user": request.user})
