from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from netchan.models import Category, User, UserProfile, Like, Page

### Helper Functions ###
def get_category_list(max_results=0, starts_with=''):
    cat_list = []
    if starts_with:
        cat_list = Category.objects.filter(name__istartswith=starts_with) # istartswith = not case sensitive
    if max_results > 0:
        if len(cat_list) > max_results:
            cat_list = cat_list[:max_results]

    return cat_list



### Create views here ###
def suggest_category(request):
    cat_list = []
    starts_with =''

    if request.method == 'GET':
        start_with = request.GET['suggestion']
    cat_list = get_category_list(8, start_with)

    return render(request, 'netchan/category_list.html', {'categories': cat_list})

@login_required
def like_category(request):
    cat_id = None
    user = User.objects.get(username=request.user)
    user_profile = UserProfile.objects.get(user=user)

    if request.method == "GET":
        cat_id = request.GET['category_id']
        likes = 0
        if cat_id:
            cat = Category.objects.get(id=int(cat_id))
            if cat:
                user_liked = Like(user=user_profile, category=cat)
                likes = cat.likes + 1
                cat.likes = likes
                cat.save()
                user_liked.save()
                
    return HttpResponse(likes)

@login_required
def auto_add_page(request):
    cat_id = None
    title = None
    url = None
    context_dict = {}
    if request.method == 'GET':
        cat_id = request.GET['cat_id']
        title = request.GET['title']
        url = request.GET['url']

        if cat_id:
            category = Category.objects.get(id=int(cat_id))
            page = Page.objects.get_or_create(category=category, title=title, url=url)
            pages = Page.objects.filter(category=category).order_by('-views')
            context_dict['pages'] = pages
            context_dict['category'] = category

    return render(request, 'netchan/page_list.html', context_dict)