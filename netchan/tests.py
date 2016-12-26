from django.test import TestCase
from netchan.models import Category
from django.core.urlresolvers import reverse

# Create your tests here.
### helper functions ###
def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c


### Testing models ###
class CategoryMethodsTests(TestCase):
    def test_ensure_views_are_positive(self): # start all tests with test_
        """
            return True if views are positive or 0
        """
        cat = Category(name='test', views=-1, likes=0)
        cat.save()
        self.assertEqual((cat.views >= 0), True) # Python 3 docs for more more unit tests

    def test_slug_line_creation(self):
        """
            make sure the right slug line is created
            when a cat is added
        """
        cat = Category(slug='Random Category String')
        cat.save()
        self.assertEqual(cat.slug, 'random-category-string')
    
    def test_slug_name_to_slug(self):
        cat = Category(name='Random Category String')
        cat.save()
        self.assertEqual(cat.slug, 'random-category-string')

### Testing Views ###
class IndexViewTests(TestCase):
    def test_index_view_with_no_categories(self):
        """
            if no categories exist
        """

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no categories present.")
        self.assertQuerysetEqual(response.context['categories'], [])

        def test_index_view_with_categories(self):
            """
            Check to make sure that the index has categories displayed
            """
            add_cat('test',1,1)
            add_cat('temp',1,1)
            add_cat('tmp',1,1)
            add_cat('tmp test temp',1,1)
            response = self.client.get(reverse('index'))
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "tmp test temp")
            num_cats =len(response.context['categories'])
            self.assertEqual(num_cats , 4)