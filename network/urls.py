
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("follow", views.follow, name="follow"),
    path("following", views.following, name="following"),
    path("editPost", views.editPost, name="editPost"),
    path("unLike", views.unLike, name="unLike")
]

#path("wiki/<str:name>", views.entry_page, name="entry_page"),
