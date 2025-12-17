from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create_note/', views.create_note, name="create_note"),
    path('note/<int:noteid>/', views.note_view, name="note"),
    path('search_notes/', views.seach_notes, name='search_notes'),
    path('error/', views.error_view, name='error'),
]
