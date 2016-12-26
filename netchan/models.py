from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    likes = models.IntegerField(default=0)

    def save(self, *args, **kwargs): 
        if not self.name: # if no name given will still check slug and set if needed
            if self.slug != slugify(self.slug):
                self.slug = slugify(self.slug)
        else:
            self.slug = slugify(self.name) # slugify adds - for whitespace

        if self.views < 0:
            self.views = 0
        
        super(Category, self).save(*args, **kwargs) # ?overrides save?

    class Meta: # shows plural name on forms etc. if more than 1
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.slug

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    # links profile to 'User' model instance
    user = models.OneToOneField(User)

    # additional attributes not in 'User' model
    website = models.URLField(blank=True) # blank = True allows empty values returns NULL
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

class Like(models.Model):
   user = models.ForeignKey(UserProfile)
   category = models.ForeignKey(Category)

   def __str__(self):
       return self.category.name
