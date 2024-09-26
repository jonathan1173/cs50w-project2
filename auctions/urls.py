from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create",views.PageList,name="create"),
    path("filter",views.filterCategory, name = "filterCategory"),
    path("listing/<int:id>", views.listing , name="listing"),
    path("remove/<int:id>", views.removeList ,name = "removeList"),
    path("add/<int:id>", views.addList ,name = "addList"),
    path("watch/",views.viewsLitWatch, name= "watchlist"),
    path("addNewComment/<int:id>", views.addComment, name="addComment"),
    path("addBid/<int:id>", views.addBids, name = "addBid"),
    path("close/<int:id>", views.close, name = "close"),
]
