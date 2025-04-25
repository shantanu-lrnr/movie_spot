from django.urls import path
from . import views


urlpatterns = [
    path("login/",views.Login.as_view(),name="login"),
    path("register/",views.RegisterUser.as_view(),name="register"),
    path("logout/",views.Logout.as_view(),name="logout"),
    path("profile/",views.UserProfile.as_view(),name="profile"),
    path("create_list/",views.create_list,name="create_list"),
    path("delete_list/<int:list_id>/",views.delete_list,name="delete_list"),
    path("lists/<int:list_id>/add/<int:movie_id>/<str:movie_name>/",views.add_to_list,name="add_to_list"),
    path("list_detail/<int:list_id>/",views.list_detail,name="list_detail"),
    path("delete_movie/<int:list_id>/<int:movie_id>/",views.delete_movie,name="delete_movie"),
]
