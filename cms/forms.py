from django.forms import ModelForm
from django import forms

from cms.models import *


class BackgroundImageForm(ModelForm):
        
    class Meta:
        model = BackgroundImage
        exclude = ['author', 'content_type', 'file_name',]


class AboutForm(ModelForm):
        
    class Meta:
        model = About


class CategoryForm(ModelForm):
        
    class Meta:
        model = Category


class PageForm(ModelForm):
        
    class Meta:
        model = Page


class StyleForm(ModelForm):
        
    class Meta:
        model = Style

