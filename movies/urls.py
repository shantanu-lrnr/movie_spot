from django.urls import path,include
from . import views

urlpatterns = [
    path("",views.landing_page,name="landing_page"),
    path("movie/<int:movie_id>/",views.movie_detail,name="movie_detail"),
]
