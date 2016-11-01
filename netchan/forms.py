from django import forms
from django.contrib.auth.models import User
from .models import Category, Page, UserProfile

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="please enter the category name.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0) # inlcude .Hidden, with value=0 
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0) # incase model default != 0 which
    slug = forms.CharField(widget=forms.HiddenInput(), initial=0)     # would raise null error unless we excluded

    # inline class to provide additional information on the form
    class Meta:
        model = Category # associate with Category model
        fields = ('name',) # either include(fields =()) or exclude fields (tuple value ',')

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Enter 'title' for page.",)
    url = forms.URLField(max_length=200, help_text="Enter 'URL' for page.", )
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page # associate with Page model
        exclude = ('category',) # fields we dont want on form(make sure they can be null in model)
                               # either include(fields =()) or exclude fields

    # this was not allowing me to submit URLs
    #def clean(self):
    #    cleaned_data = self.cleaned_data # cleaned_data is a attribute of ModelForm returns dictionary
    #    url = cleaned_data.get('url') # .get pulls value from database

    #    # if url not empty and does not start with 'http://' then prepend it
    #    if url and not url.startswith('http://'):
    #        url = 'http://' + url
    #        cleaned_data['url'] = url
    #        print('Cleaned {}'.format(url))

    #        return cleaned_data # always return to clean_data dict or changes won't apply
    None # just so i can minimize class

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput()) # so password is hidden

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
