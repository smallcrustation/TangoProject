import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'TangoProject.settings')

import django
django.setup()
from netchan.models import Category, Page

def populate():
    # Create lists of dictionaries containg the pages we ant to add into each category
    #Then we will create a dictionary of dictionaries for our categories.

    python_pages = [
        {"title": "Official Python Tutorial",
        "url": "http://docs.python.org/2/tutorial/",
        "views": 0},
        {"title": "How to Think like a Computer Scientist",
        "url": "http://www.greenteapress.com/thinkpython/",
        'views': 0},
        {"title":"Learn Python in 10 Minutes",
        "url":"http://www.korokithakis.net/tutorials/python/",
        'views': 0}
         ]
    
    django_pages = [
        {"title":"Official Django Tutorial",
        "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/",
        'views': 0},
        {"title":"Django Rocks",
        "url":"http://www.djangorocks.com/",
        'views': 0},
        {"title":"How to Tango with Django",
        "url":"http://www.tangowithdjango.com/",
        'views': 0} 
        ]

    other_pages = [
        {"title":"Bottle",
        "url":"http://bottlepy.org/docs/dev/",
        'views': 0},
        {"title":"Flask",
        "url":"http://flask.pocoo.org",
        'views': 0} 
        ]

    categories = {"Python": {"pages": python_pages, "views": 0, "likes": 0},
                  "Django": {"pages": django_pages, "views": 0, "likes": 0},
                  "Other Frameworks": {"pages": other_pages, "views": 0, "likes": 0}  }



    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated pages for that category. 

    for category, category_data in categories.items():
        c = add_category(category, category_data['views'], category_data['likes'])
        for p in category_data["pages"]:
            add_page(c, p["title"], p["url"], p["views"])

    # print out the categories added
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))

def add_page(category, title, url, views=0):
    p = Page.objects.get_or_create(category=category, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_category(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views=views
    c.likes=likes
    c.save()
    return c

# execute script
if __name__ == '__main__':
    print("Starting netchan population script!?...")
    populate()