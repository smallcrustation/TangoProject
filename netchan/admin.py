from django.contrib import admin
from netchan.models import Category, Page
from netchan.models import UserProfile

# Register your models here.
class PageAdmin(admin.ModelAdmin):               # what it's going to show
    list_display = ('title', 'category', 'url',) # list display is a particular attribute of admin.ModelAdmin

class CategoryAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'views',)
    prepopulated_fields = {'slug':('name',)}

# display items in admin view
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin) # run you admin class here as well
admin.site.register(UserProfile)
