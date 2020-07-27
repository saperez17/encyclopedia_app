from django.urls import path, re_path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path('wiki/', views.wiki_ini, name="wiki_ini"),
    path('wiki/<str:title>', views.wiki, name="wiki"),
    path('wiki/search', views.wiki, name="search"),
    path('wiki/newpage/', views.newpage, name="new_entry"),
    path('wiki/edit_entry/', views.edit_entry, name="edit_entry"),
    path('wiki/random/', views.random, name="random"),
    

    # path("wiki", views.wiki, name="wiki_default")
    
    
]
