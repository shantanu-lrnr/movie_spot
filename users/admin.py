from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserList, ListItem

admin.site.register(CustomUser,UserAdmin)


class ListItemInline(admin.TabularInline):
    model = ListItem
    extra = 1  # Number of empty forms to display
    verbose_name = "List Item"


@admin.register(UserList)
class UserListAdmin(admin.ModelAdmin):
    # list_display = ('user', 'name', 'date_created')
    # list_filter = ('user', 'name', 'date_created')
    # search_fields = ('user__username', 'name')
    # ordering = ('-date_created',)
    # date_hierarchy = 'date_created'
    # raw_id_fields = ('user',)
    # list_per_page = 10  
    # pass
    inlines = [ListItemInline]

@admin.register(ListItem)
class ListItemAdmin(admin.ModelAdmin):
    list_display = ('list', 'movie_id', 'date_added')
    list_filter = ('list', 'movie_id', 'date_added')
    search_fields = ('list__name', 'movie_id')
    ordering = ('-date_added',)
    date_hierarchy = 'date_added'
    # raw_id_fields = ('list',)
    # list_per_page = 10
 