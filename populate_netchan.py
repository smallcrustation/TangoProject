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
        "url": "http://docs.python.org/2/tutorial/"},
        {"title": "How to Think like a Computer Scientist",
        "url": "http://www.greenteapress.com/thinkpython/"},
        {"title":"Learn Python in 10 Minutes",
        "url":"http://www.korokithakis.net/tutorials/python/"}
         ]
    
    django_pages = [
        {"title":"Official Django Tutorial",
        "url":"https://docs.djangoproject.com/en/1.9/intro/tutorial01/"},
        {"title":"Django Rocks",
        "url":"http://www.djangorocks.com/"},
        {"title":"How to Tango with Django",
        "url":"http://www.tangowithdjango.com/"} 
        ]

    other_pages = [
        {"title":"Bottle",
        "url":"http://bottlepy.org/docs/dev/"},
        {"title":"Flask",
        "url":"http://flask.pocoo.org"} 
        ]

    categories = {"Python": {"pages": python_pages},
            "Django": {"pages": django_pages},
            "Other Frameworks": {"pages": other_pages} }

    # The code below goes through the cats dictionary, then adds each category,
    # and then adds all the associated pages for that category. 

    for category, category_data in categories.items():
        c = add_category(category)
        for p in category_data["pages"]:
            add_page(c, p["title"], p["url"])

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

def add_category(name):
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c

# execute script
if __name__ == '__main__':
    print("Starting netchan population script!?...")
    populate()