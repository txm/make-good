from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import connection
from django.db.models import Max
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from google.appengine.api import users
from google.appengine.api import memcache

import random
import urllib

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

    key = 'bg_image'+bg_image_id

    bg_image = memcache.get(key)

    if bg_image is not None:
        return HttpResponse(bg_image.image, mimetype=bg_image.content_type)
    else:
        try:
            bg_image = BackgroundImage.objects.get(id=bg_image_id)
            memcache.add(key, bg_image, 360000)
            return HttpResponse(bg_image.image, mimetype=bg_image.content_type)
        except:
            raise Http404


def page(request, page_id):

    page = Page.objects.get(id=page_id)
    content = PageWYSIWYG.objects.get(page=page_id)

    return render_to_response('page.html', {
        'page': page, 
        'content': content,
    }, context_instance=RequestContext(request))


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
            return HttpResponseRedirect(request.META['PATH_INFO']+'?message=Updated')

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
            bg_image_form.content_type = ('image/' + (str(request.FILES['image'])).partition('.')[2]).lower
            bg_image_form.save()

            return HttpResponseRedirect(request.META['PATH_INFO']+'?message=Updated')

    else:
        form = BackgroundImageForm()

    bg_images = BackgroundImage.objects.all().values('id', 'title', 'author', 'file_name', 'content_type', 'date_inserted' )


    return render_to_response('admin_bg_image.html', {
        'form': form, 
        'bg_images': bg_images,
    }, context_instance=RequestContext(request))


@login_required
def admin_bg_image_edit(request, bg_image_id):

    if request.method == 'POST':

        bg_image = BackgroundImage.objects.get(id=bg_image_id)
        form = BackgroundImageForm(instance=bg_image, data=request.POST, files=request.FILES)

        if form.is_valid():

            user = users.get_current_user()

            bg_image_form = form.save(commit=False)
            bg_image_form.author = user

            if 'image' in request.FILES and request.FILES['image'] is True:

                bg_image_form.file_name = request.FILES['image']
                bg_image_form.content_type = ('image/' + (str(request.FILES['image'])).partition('.')[2]).lower

            bg_image_form.save()


            return HttpResponseRedirect('/admin/bg_image/?message=' + urllib.quote_plus('Image has been updated') )

    else:

        bg_image = BackgroundImage.objects.get(id=bg_image_id)
        form = BackgroundImageForm(instance=bg_image)

        return render_to_response('admin_bg_image_edit.html', {
            'form': form, 
            'bg_image': bg_image,
        }, context_instance=RequestContext(request))


def css(request):

    if Style.objects.count() > 0:
        style = Style.objects.order_by('id').reverse()[0]
    else:
        style = False

    return render_to_response('dynamic.css', { 'style': style, }, context_instance=RequestContext(request), mimetype='text/css; charset=utf-8')


@login_required
def admin_bg_image_delete(request, bg_image_id):

    message = 'Invalid request'

    if request.method == 'GET':

        try:
            bg_image = BackgroundImage.objects.get(id=bg_image_id)
        except:
            message = 'Image not found'

        if bg_image:
            bg_image.delete()
            message = 'Image has been deleted'

    return HttpResponseRedirect('/admin/bg_image/?message=' + urllib.quote_plus( message ) )


@login_required
def admin_page_delete(request, page_id):

    message = 'Invalid request'

    if request.method == 'GET':


        try:
            page_wysiwyg = PageWYSIWYG.objects.get(page=page_id)
            page_wysiwyg.delete();
            page = Page.objects.get(id=page_id)
            page.delete()
            message = 'Page deleted'
        except:
            message = 'Page not found'

    return HttpResponseRedirect('/admin/page/?message=' + urllib.quote_plus( message ) )


@login_required
def admin_category_edit(request, category_id):

    if request.method == 'POST':

        category = Category.objects.get(id=category_id)
        form = CategoryForm(instance=category, data=request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/admin/category/?message=' + urllib.quote_plus('Category has been updated') )
        else:
            assert False, form.errors

    else:
        category = Category.objects.get(id=category_id)
        form = CategoryForm(instance=category)

    return render_to_response('admin_category_edit.html', { 'form': form, 'category' : category }, context_instance=RequestContext(request))



@login_required
def admin_category_delete(request, category_id):

    if request.method == 'GET':
        category = Category.objects.get(id=category_id)
        category.delete()

    return HttpResponseRedirect('/admin/category/?message=deleted')


@login_required
def admin_category(request):

    if request.method == 'POST':

        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META['PATH_INFO']+'?message=updated')

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

        page_form = PageForm(request.POST)
        page_wysiwyg_form = PageWYSIWYGForm(request.POST)

        if page_form.is_valid():
            page_form = page_form.save()
            combined_form = page_wysiwyg_form.save(commit=False)
            combined_form.page = Page.objects.get(id=page_form.id)
            combined_form.save()
            return HttpResponseRedirect(request.META['PATH_INFO']+'?message=Updated')

    else:
        page_form = PageForm()
        page_wysiwyg_form = PageWYSIWYGForm()

    pages = Page.objects.all()

    return render_to_response('admin_page.html', { 
        'page_form': page_form, 
        'page_content_form': page_wysiwyg_form, 
        'pages' : pages,
    }, context_instance=RequestContext(request))
    

@login_required
def admin_style(request):

    if request.method == 'POST':

        form = StyleForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META['PATH_INFO']+'?message=updated')
        else:
            if Style.objects.count() <= 0:
                style = False

    else:

        if Style.objects.count() > 0:
            style = Style.objects.order_by('id').reverse()[0]
            form = StyleForm(instance=style)
        else:
            style = False
            form = StyleForm()

    return render_to_response('admin_style.html', { 'form': form, 'style' : style }, context_instance=RequestContext(request))


@login_required
def admin_page_edit(request, page_id):

    if request.method == 'POST':

        page = Page.objects.get(id=page_id)
        page_form = PageForm(instance=page, data=request.POST)

        page_wysiwyg = PageWYSIWYG.objects.get(page=page_id)
        page_wysiwyg_form = PageWYSIWYGForm(instance=page_wysiwyg, data=request.POST)

        if page_form.is_valid():
            page_form.save()
            page_wysiwyg_form.save()
            return HttpResponseRedirect('/admin/page/?message=' + urllib.quote_plus('Page has been updated') )
        else:
            assert False, page_form.errors

    else:

        page = Page.objects.get(id=page_id)
        page_form = PageForm(instance=page)

        page_wysiwyg = PageWYSIWYG.objects.get(page=page_id)
        page_wysiwyg_form = PageWYSIWYGForm(instance=page_wysiwyg)

    return render_to_response('admin_page_edit.html', {
        'page_form': page_form, 
        'page_content_form': page_wysiwyg_form, 
        'page' : page,
    }, context_instance=RequestContext(request))


