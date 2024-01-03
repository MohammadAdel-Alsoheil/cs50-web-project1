from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search_results", views.search_results, name="search_results"),
    path("random_page",views.randomize, name="randomize"),
    path("Add",views.add_page,name="add_page"),
    path("Edit/<str:entry>",views.edit_page,name="edit_page"),
    path("wiki/<str:TITLE>",views.get_title, name="get_title")
]
