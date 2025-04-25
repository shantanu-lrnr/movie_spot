from django.shortcuts import render,redirect
from django.contrib.auth.views import LoginView,LogoutView
from django.views import View
from django.views.generic.edit import FormView
from .forms import UserRegisterForm,UserAuthenticationForm,CreateListForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import UserList,CustomUser,ListItem
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
import requests
from decouple import config
from django.urls import reverse_lazy



API_KEY = config("TMDB_API_KEY")

class Login(LoginView):
    template_name = "users/accounts/login.html"
    form_class = UserAuthenticationForm

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("landing_page")
        return super().dispatch(request, *args, **kwargs)
    
    # def get_success_url(self):
    #     return reverse_lazy("landing_page")
    
class Logout(LogoutView):
    next_page = '/'
    

# @method_decorator(login_required(login_url="/user/login/"), name='dispatch')
# @method_decorator(login_required(login_url="login"), name='dispatch')
@method_decorator(login_required, name='dispatch')
class UserProfile(View):
    def get(self,request):
        user = request.user
        # user_lists = user.user_list.all()
        user_lists = UserList.objects.filter(user=user)
        return render(request,"users/accounts/profile.html",{"user":user,"user_lists":user_lists})
    
class RegisterUser(FormView):
    template_name = "users/accounts/register.html"
    form_class = UserRegisterForm
    success_url = "/"

    def form_valid(self, form):
        user = form.save()
        login(self.request,user)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        return response

@login_required
def create_list(request):
    user = request.user
    if request.method == "POST":
        form = CreateListForm(request.POST)
        if form.is_valid():
            list = form.save(commit=False)
            list.user = user
            list.save()
            user_lists = UserList.objects.filter(user=user)
            return render(request,"users/lists/partials/_user_list.html",{"user_lists":user_lists})
        return render(request,"users/lists/partials/_create_list_form.html",{"form":form})
    form =  CreateListForm()
    return render(request,"users/lists/partials/_create_list_form.html",{"form":form})

@login_required
def delete_list(request,list_id):
    print(type(list_id))
    user_list = get_object_or_404(UserList,pk=list_id)
    if request.method == "POST":
        user_list.delete()
        return render(request,"users/lists/partials/_user_list.html",{"user_lists":UserList.objects.filter(user=request.user)})
    return HttpResponseForbidden("<h1>403 Forbidden</h1>")

@login_required
def add_to_list(request,movie_id,movie_name,list_id):
    user = request.user
    user_list = get_object_or_404(UserList,pk=list_id)
    print(user_list)
    if ListItem.objects.filter(movie_id=movie_id,list=user_list).exists():
        message = f"{movie_name} is already in your"
        status = "danger"
    else:
        ListItem.objects.create(list=user_list,movie_name=movie_name,movie_id=movie_id)
         
        message = f"{movie_name} was added to"
        status = "success"

    return render(request,"users/toasts/_confirmation_toast.html",{"message":message,"status":status,"user_list":user_list})


def list_detail(request,list_id):
    user_list = get_object_or_404(UserList,pk=list_id)
    # list_items = user_list.list_item.all() 
    list_items = ListItem.objects.filter(list=user_list)
    base_url = f"https://api.themoviedb.org/3/movie/"

    movies = []
    for item in list_items:
        movie_id = item.movie_id
        url = f"{base_url}{movie_id}?api_key={API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            movie = response.json()
            movies.append(movie)
    return render(request,"users/lists/user_list_movies.html",{"movies":movies,"user_list":user_list,"is_owner":request.user.is_authenticated and request.user == user_list.user})

@login_required
def delete_movie(request,movie_id,list_id):
    user_list = get_object_or_404(UserList,pk=list_id,user=request.user)
    movie = get_object_or_404(ListItem,movie_id=movie_id,list=user_list)
    if request.method == "POST":
        movie.delete()
        list_items = ListItem.objects.filter(list=user_list)
        base_url = f"https://api.themoviedb.org/3/movie/"

        movies = []
        for item in list_items:
            movie_id = item.movie_id
            url = f"{base_url}{movie_id}?api_key={API_KEY}"
            response = requests.get(url)
            if response.status_code == 200:
                movie = response.json()
                movies.append(movie)
        return render(request,"users/lists/partials/_updated_list.html",{"movies":movies,"user_list":user_list,"is_owner":request.user.is_authenticated and request.user == user_list.user})
    return HttpResponseForbidden("<h1>403 Forbidden</h1>")

    



    