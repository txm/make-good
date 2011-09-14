from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from google.appengine.api import users

from cms.forms import BlogForm
from cms.models import Blog


def blogs(request):

    blogs = Blog.objects.all()
    return render_to_response('home.html', { 'blogs': blogs }, context_instance=RequestContext(request))


def blog_view(request, id):

    blog = Blog.objects.get(id=id)
    return render_to_response('home_view.html', { 'blog': blog }, context_instance=RequestContext(request))


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

    if request.method == 'POST':
        form = BlogForm(data=request.POST)
        if form.is_valid():
            blog = form.save()
            form = BlogForm()
            tweet(request, blog)

    else:
        form = BlogForm()

    blogs = Blog.objects.all()

    return render_to_response('admin_home.html', {
        'form': form,
        'blogs': blogs,
    }, context_instance=RequestContext(request))


@login_required
def admin_edit(request):

    if request.method == 'POST':       # If the form has been submitted...
        blog = Blog.objects.get(id=request.GET['id'])
        form = BlogForm(instance=blog,data=request.POST)
        if form.is_valid():            # All validation rules pass
            form.save()
            return HttpResponseRedirect('/admin/') # Redirect after POST

    elif request.GET.has_key('id'):
        blog = Blog.objects.get(id=request.GET['id'])
        form = BlogForm(instance=blog)
        blogs = Blog.objects.all()
        return render_to_response('admin_home.html', {
            'form': form,
            'blogs': blogs,
            'id': request.GET['id'],
        }, context_instance=RequestContext(request))

    else:
        return HttpResponseRedirect('/admin/') # Redirect after POST


@login_required
def admin_delete(request):

    if request.method == 'GET' and request.GET.has_key('id'):
        blog = Blog.objects.get(id=request.GET['id'])
        blog.delete()

    return HttpResponseRedirect('/admin/') # Redirect after POST


