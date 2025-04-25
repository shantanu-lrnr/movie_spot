from django.shortcuts import render
from decouple import config
import requests
from users.models import UserList, ListItem

# Create your views here.

API_KEY = config("TMDB_API_KEY")
def landing_page(request):
    category = request.GET.get("category","popular")
    search_query = request.GET.get("search","")
    page = int(request.GET.get("page",1))
    next_page = page + 1
    user_lists = UserList.objects.filter(user=request.user) if request.user.is_authenticated else None
    error_message = ""
    base_url = "https://api.themoviedb.org/3/movie/"
    
    if search_query:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={search_query}&page={page}"
    else:
        url = f"{base_url}{category}?api_key={API_KEY}&page={page}"

    try:
        movie_detail_response = requests.get(url)
        movie_detail_response.raise_for_status()
        movie_data = movie_detail_response.json().get("results",[])
        total_pages = movie_detail_response.json().get("total_pages",0)
        has_next = page<total_pages

    except Exception as e:
        error_message = "Something went wrong !!"
        movie_data = []
        has_next = False

    if request.headers.get("Hx-Request"):
        return render(request,'movies/partials/_movie_list.html',{"movies":movie_data,"category":category,"search_query":search_query,"error_message":error_message,"next_page":next_page,"has_next":has_next,"user_lists":user_lists})
    return render(request,'movies/landing.html',{"movies":movie_data,"category":category,"search_query":search_query,"error_message":error_message,"next_page":next_page,"has_next":has_next,"user_lists":user_lists})


def movie_detail(request,movie_id):
    movie_detail_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
    movie_credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}"
    user_lists = UserList.objects.filter(user=request.user) if request.user.is_authenticated else None
    
    error_message=""
    try:
        movie_detail_response = requests.get(url=movie_detail_url)
        movie_detail_response.raise_for_status()
        movie_data = movie_detail_response.json()

    except Exception as e:
        error_message = "Something went wrong !!"
        movie_data = []

    try:
        movie_credits_response = requests.get(url=movie_credits_url)
        movie_credits_response.raise_for_status()
        credits_data = movie_credits_response.json()
    except Exception as e:
        error_message = "Something went wrong !!"
        credits_data = []

    return render(request,"movies/movie_detail.html",{"movie":movie_data,"error_message":error_message,"credits":credits_data,"user_lists":user_lists})
        



    