from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import connection
from .models import Note

def index(request):
    print("USER", request.user)
    notes = []
    if request.user.is_authenticated:
        notes = Note.objects.filter(owner=request.user)
    return render(request, "notes/index.html", {"user": request.user,
                                                "notes": notes})

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

    if request.user == note.owner:
        return render(request, "notes/note.html", {"note": note})
    
    print("RESTRICTED ACCESS")
    return redirect("/")

def seach_notes(request):
    query = request.GET.get("query", "")
    notes = []

    if query and request.user.is_authenticated:
        cursor = connection.cursor()
        
        # A03 Injection
        # sql = """SELECT n.id, n.content, u.username 
        #         FROM notes_note n 
        #         JOIN auth_user u ON n.owner_id = u.id 
        #         WHERE n.owner_id='""" + str(request.user.id) + "' and n.content LIKE '%" + query + "%'"

        # response = cursor.execute(sql).fetchall()

        sql = """SELECT n.id, n.content, u.username
                FROM notes_note n
                JOIN auth_user u ON n.owner_id = u.id
                WHERE n.owner_id = %(owner_id)s
                AND n.content LIKE %(query)s"""
        
        response = cursor.execute(sql, {"owner_id": request.user.id, 
                                        "query": f"%{query}%"}).fetchall()

        for r in response:
            print("RESPONSE", r)
            notes.append({"id": r[0], "content": r[1], "owner": r[2]})

    return render(request, "notes/search_notes.html", {"query": query,
                                                       "notes": notes,
                                                       "user": request.user})
