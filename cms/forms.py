from django.forms import ModelForm
from django import forms

from cms.models import *


class BackgroundImageForm(ModelForm):
        
    class Meta:
        model = BackgroundImage
        exclude = ['author', 'date_inserted', 'blob_key', 'url', 'url_thumb', ]


class AboutForm(ModelForm):
        
    class Meta:
        model = About


class CategoryForm(ModelForm):
        
    class Meta:
        model = Category


class PageForm(ModelForm):
        
    class Meta:
        model = Page


class PageWYSIWYGForm(ModelForm):
        
    content = forms.CharField( widget=forms.Textarea(attrs={'class':'wysiwyg', }))

    class Meta:
        model = PageWYSIWYG
        exclude = ['page', ]


class StyleForm(ModelForm):
        
    class Meta:
        model = Style

