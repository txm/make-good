from django.conf.urls.defaults import *

urlpatterns = patterns('',
    #('^$', 'django.views.generic.simple.direct_to_template', {'template': 'home.html'}),

    ('^$', 'cms.views.blogs'),
    ('^blog/(\d+)$', 'cms.views.blog_view'),

    ('^admin/$', 'cms.views.admin_home'),
    ('^admin/edit/', 'cms.views.admin_edit'),
    ('^admin/delete/', 'cms.views.admin_delete'),
)


