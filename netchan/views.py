from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime
from django.views import View
from django.utils.decorators import method_decorator

from netchan.models import Category, Page, UserProfile, Like
from .forms import CategoryForm, PageForm, UserProfileForm, UserForm
from registration.backends.simple.views import RegistrationView
from netchan.bing_search import run_query

## Helper functions ##
def get_server_side_cookie(request, cookie, default_val=None):
    # try's to get a cookie fom the server if it does not exist returns none instead of the value
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    can_add_view = False
    
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    # ('last vis {}'.format(last_visit_cookie))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S') 
   
    # check if it's been more than 1 day since last visit
    if (datetime.now() - last_visit_time).seconds > 0:
        visits += 1
        request.session['last_visit'] = str(datetime.now()) # update the 'last_visit_cookie' cookie
      
    else: # set cookie to 'llast_visit_cookie' same as last visit
        request.session['last_visit'] = last_visit_cookie
       
    # update/set the visits cookie
    request.session['visits'] = visits # set 'visits' cookie to visits value

## Create your views here ##
'''
def index(request):
    # Query database for a *list* of ALL categories currently stored, Order categories by num likes in
    # descending order.Retrieve the top 5 only (-) or all if less than 5.
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
  
    # Place the list in our context_dict dictionary that will be passed to the template engine.
    context_dict = {'categories': category_list, 'pages': page_list}

    # ***server side cookie no cookie other than sessionid cookie will show in browser***
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    # print('{} views'.format(context_dict['visits']))

    # Handle cookie tracker, set response variable so you can change it's request cookies accordingly
    response = render(request, 'netchan/index.html', context=context_dict) # get response object so we can pass into 

    return response # call response'''
class index(View):
    # Query database for a *list* of ALL categories currently stored, Order categories by num likes in
    # descending order.Retrieve the top 5 only (-) or all if less than 5.
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
  
    # Place the list in our context_dict dictionary that will be passed to the template engine.
    context_dict = {'categories': category_list, 'pages': page_list}
    def get(self, request):
        # ***server side cookie no cookie other than sessionid cookie will show in browser***
        visitor_cookie_handler(request)
        self.context_dict['visits'] = request.session['visits']
        # Handle cookie tracker, set response variable so you can change it's request cookies accordingly
        response = render(request, 'netchan/index.html', context=self.context_dict) # get response object so we can pass into 
        return response

'''
def about(request):
    context_dict = {}
    context_dict['visits'] = request.session['visits']
    return render(request, 'netchan/about.html', context_dict) # no additional data to give to the template, passan empty dictionary, {}
'''
class about(View):
    context_dict = {}
    template_name = 'netchan/about.html'
    def get(self, request):
        self.context_dict['visits'] = request.session['visits']
        return render(request, self.template_name, self.context_dict)

def show_cats(request):
    category_list = Category.objects.order_by('name')
    return render(request, 'netchan/category_list_page.html', {'categories':category_list})

def show_category(request, category_name_slug): # cat_n_slug passed in through ?P urls, which get it from index <a>
    # context dict to pass into trmplate render
    context_dict = {}           

    try:
        # try and get the category by the name slug, returns DoesNotExist exception if not ther
        category = Category.objects.get(slug=category_name_slug)

        # checks if user has already liked a cat could make a func for most of this cause i use most of it twice
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            user_profile = UserProfile.objects.get_or_create(user=user)[0]
            form = UserProfileForm({'website': user_profile.website, 'picture': user_profile.picture})
            liked_cats_query = Like.objects.filter(user=user_profile)
            liked_cats = []
            for query in liked_cats_query:
                liked_cats.append(query.category.slug)
            if category.slug in liked_cats:
                liked = True
            else:
                liked = False
            context_dict['liked'] = liked

        # filter associated pages by the foreign key category, returns a list empty or otherwise
        pages = Page.objects.filter(category=category)       

        # adds pages to the context_dict
        context_dict['pages'] = pages
        context_dict['category'] = category # used in the template for {% if exists %}

        category.views = category.views + 1
        category.save()

    except Category.DoesNotExist:
        # if we didn't find the category slug do below (which is nothing)
        # templates will display 'no category' msg for us
        context_dict['category'] = None
        context_dict['pages'] = None

    # search functionality
    result_list = []
    query = ''
        
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            result_list = run_query(query)
    context_dict['result_list'] = result_list
    context_dict['query'] = query

    return render(request, 'netchan/category.html', context_dict)

'''def search(request):
    result_list = []
    query = ''
        
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            result_list = run_query(query)

    return render(request, 'netchan/search.html', {'result_list': result_list, 'query': query})'''

def track_url(request):
    page_id = None
    if request.method == 'GET':
        if 'page_id' in request.GET: # 'page_id' in the string info provided by request.txt?
            page_id = request.GET['page_id']
        if page_id:
            try:
                page = Page.objects.get(id=page_id)
                print(page.views)
                page.views = page.views + 1
                print(page.views)
                page.save()
                return redirect(page.url)
            except:
                return HttpResponse("Page id {0} not found".format(page_id))

    print("No page_id in string")
    return redirect(reverse('index'))

class MyRegistrationView(RegistrationView):
    success_url = 'register_profile'

# @login_required
'''def add_category(request):
    form = CategoryForm

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # check if the form is valid
        if form.is_valid():
            form.save(commit=True)
            # category is saved, could give confirmation msg 
            # redirect to index page
            return index(request)
        
        else: # error detected
            print(form.errors) # print to console

    # returns the form in all cases if erros shows them
    return render(request, 'netchan/add_category.html', {'form': form})'''
@method_decorator(login_required, name='dispatch') # method decorator imported
class add_category(View):
    form = CategoryForm
    template_name = 'netchan/add_category.html'

    def get(self, request):
         # returns the form in all cases if erros shows them
        return render(request, self.template_name, {'form': self.form})

    def post(self, request):
        self.form = CategoryForm(request.POST)
        # check if the form is valid
        if self.form.is_valid():
            self.form.save(commit=True)
            # category is saved, could give confirmation msg 
            # redirect to index page
            return HttpResponseRedirect('netchan/index.html')
        else: # error detected
            errors = self.form.errors  # print to console
            return render(request, self.template_name, {'errors': errors, 'form': self.form})


@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category=None
            
    form = PageForm

    if request.method == 'POST':
        form = PageForm(request.POST)
        
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                form.save()
                return index(request)

            else:
                print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'netchan/add_page.html', context_dict)


@login_required
def register_profile(request):
    form = UserProfileForm

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES) # FILES pulls files in the post request

        if form.is_valid():
            user_profile = form.save(commit=False) # set to false so we can get the user_profile.user
            user_profile.user = request.user       # of currently logged in user from *request*.user
            form.save(commit=True)
            return redirect('index')
        else:
            print(form.errors)

    context_dict = {'form':form}
    return render(request, 'netchan/profile_registration.html', context_dict)

@login_required # LOGIN_URL='' in settings.py for where you get redirected to if not logd in
def restricted(request):
    # print('yolo') # test
    return render(request, 'netchan/restricted.html', {})

@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    user_profile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm({'website': user_profile.website, 'picture': user_profile.picture})
    liked_cats = Like.objects.filter(user=user_profile)     

    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('profile', user.username)
        else:
            print(form.errors)

    context_dict = {'userprofile': user_profile, 'selecteduser': user, 'form': form, 'liked_cats': liked_cats,}
    return render(request, 'netchan/profile.html', context_dict)

@login_required
def profile_list(request):
    user_list = UserProfile.objects.all()
    return render(request, 'netchan/profiles_list.html', {'user_list':user_list})

'''
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
    '''


     















































######################################## DECOMISSIONED ###############################

#@login_required
#def user_logout(request):
#    logout(request)
#    return HttpResponseRedirect(reverse('index'))

#def user_login(request):
#    if request.method == 'POST':
#        # use .get('') because POST('') will raise a KeyError exception
#        username = request.POST.get('username')
#        password = request.POST.get('password')

#        # use django to test user/pass... a User object is returned if it is.
#        user = authenticate(username=username, password=password)

#        if user:
#            if user.is_active: # check if account is disabled
#                login(request, user) # 'login' is a django function
#                return HttpResponseRedirect(reverse('index'))
#            else:
#                return HttpResponse("Your netchan Account is fucked(disabled).")

#        else:
#            print('Invalid login details: {0}, {1}'.format(username, password))
#            return HttpResponse('Invalid login info supplied.')

#    else:
#        return render(request, 'netchan/login.html', {})

#def register(request):
#    registered = False # bool for telling the template whethe the reg. was successful

#    # when you hit 'submit' sends POST request
#    if request.method == 'POST': 
#        user_form = UserForm(data=request.POST)  # Attempt to grab information from the raw form information
#        profile_form = UserProfileForm(data=request.POST) # see above

#        if user_form.is_valid() and profile_form.is_valid(): # check yo ()
#            user = user_form.save() # save user 'form' data to database

#            # hash password then update (.save) user again this time with password
#            user.set_password(user.password) # User attribute in UserProfile model imported model from django 
#            user.save()       
                           
#            # next work on profile commit = False to avaoid integrity problems?
#            profile = profile_form.save(commit=False)
#            profile.user = user # where we connect UserProfile to User model

#            if 'picture' in request.FILES:
#                profile.picture = request.FILES['picture'] # FILES must be special?

#            profile.save() 

#            registered = True

#        else:
#            print(user_form.errors, profile_form.errors) # prints problems to terminal

#    # **NOT** an HTTP POST request, so render forms
#    else:
#        user_form = UserForm()
#        profile_form = UserProfileForm()

#    # render template dpending on context (could do context_dict = {})
#    return render(request, 'netchan/register.html',
#                  {'user_form': user_form,
#                   'profile_form': profile_form,
#                   'registered': registered})   