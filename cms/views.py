from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import connection
from django.db.models import Max
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from google.appengine.api import users

import random

from cms.forms import *
from cms.models import *


def home(request):

    bg_image_count = BackgroundImage.objects.count()

    if bg_image_count > 0:
        random_number = random.randrange(bg_image_count)
        bg_images = BackgroundImage.objects.all()
        bg_image = bg_images[random_number]
    else:
        bg_image = False

    categories = Category.objects.all()

    return render_to_response('home.html', { 
        'bg_image': bg_image, 
        'categories': categories, 
    }, context_instance=RequestContext(request))


def bg_image(request, bg_image_id):

    bg_image = BackgroundImage.objects.get(id=bg_image_id)
    response = HttpResponse(bg_image.image, mimetype=bg_image.content_type)
    return response


def page(request, page_id):


    return render_to_response('page.html', { }, context_instance=RequestContext(request))


# Borrowed from http://www.factory-h.com/blog/?p=23
def login_required(fn):
    """ checks to see if the user is logged in, if not, redirect to login """

    def _dec(view_func):
        def _checklogin(request, *args, **kwargs):

            user = users.get_current_user()
            if user:
                return view_func(request, *args, **kwargs)

            else:
                return HttpResponseRedirect(users.create_login_url(request.get_full_path()))

        _checklogin.__doc__ = view_func.__doc__
        _checklogin.__dict__ = view_func.__dict__

        return _checklogin

    return _dec(fn)


@login_required
def admin_home(request):

    return render_to_response('admin_home.html', { }, context_instance=RequestContext(request))


@login_required
def admin_about(request):

    if request.method == 'POST':

        form = AboutForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META['PATH_INFO']+'?action=updated')

    if About.objects.count() > 0:
        about = About.objects.order_by('id').reverse()[0]
        form = AboutForm(instance=about)
    else:
        about = False
        form = AboutForm()

    return render_to_response('admin_about.html', { 'form': form, 'about' : about }, context_instance=RequestContext(request))


@login_required
def admin_bg_image(request):

    if request.method == 'POST':

        form = BackgroundImageForm(request.POST, request.FILES)

        if form.is_valid():

            user = users.get_current_user()

            bg_image_form = form.save(commit=False)
            bg_image_form.author = user
            bg_image_form.file_name = request.FILES['image']
            bg_image_form.content_type = 'image/' + (str(request.FILES['image'])).partition('.')[2]
            bg_image_form.save()

            return HttpResponseRedirect(request.META['PATH_INFO']+'?action=updated')

    else:
        form = BackgroundImageForm()

    bg_images = BackgroundImage.objects.all()

    return render_to_response('admin_bg_image.html', {
        'form': form, 
        'bg_images': bg_images,
    }, context_instance=RequestContext(request))


@login_required
def admin_category(request):

    if request.method == 'POST':

        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META['PATH_INFO']+'?action=updated')

    else:
        form = CategoryForm()

    categories = Category.objects.all()

    return render_to_response('admin_category.html', {
      'form': form, 
      'categories' : categories,
    }, context_instance=RequestContext(request))


@login_required
def admin_page(request):

    if request.method == 'POST':

        form = PageForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META['PATH_INFO']+'?action=updated')

    else:
        form = PageForm()

    pages = Page.objects.all()

    return render_to_response('admin_page.html', { 'form': form, 'pages' : pages }, context_instance=RequestContext(request))
    

@login_required
def admin_style(request):

    styles = Style.objects.all()
    form = StyleForm()

    return render_to_response('admin_style.html', { 'form': form, 'styles' : styles }, context_instance=RequestContext(request))
    



