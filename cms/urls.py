from django.conf.urls.defaults import *

urlpatterns = patterns('',
    #('^$', 'django.views.generic.simple.direct_to_template', {'template': 'home.html'}),

    ('^$',                     'cms.views.home'),
    ('^media/bg_image/(\d+)$', 'cms.views.bg_image'),
    ('^p/(\d+)/?.+$',          'cms.views.page'),

    ('^admin/$',               'cms.views.admin_home'),
    ('^admin/about/$',         'cms.views.admin_about'),
    ('^admin/bg_image/$',      'cms.views.admin_bg_image'),
    ('^admin/category/$',      'cms.views.admin_category'),
    ('^admin/page/$',          'cms.views.admin_page'),
    ('^admin/style/',          'cms.views.admin_style'),

)


