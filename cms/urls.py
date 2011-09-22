from django.conf.urls.defaults import *

urlpatterns = patterns('',

    #('^$', 'django.views.generic.simple.direct_to_template', {'template': 'home.html'}),


    # Public handlers

    ('^$',                           'cms.views.home'),
    # using images.get_serving_url() instead .. for now .. investigate cache-control + memcache
    #('^media/bg_image/(\d+)$',       'cms.views.bg_image'),
    ('^p/(\d+)/?.+$',                'cms.views.page'),
    ('^assets/dynamic.css$',         'cms.views.css'),


    # Admin handlers

    ('^admin/$',                      'cms.views.admin_home'),

    ('^admin/about/$',                'cms.views.admin_about'),

    ('^admin/style/',                 'cms.views.admin_style'),

    ('^admin/bg_image/$',             'cms.views.admin_bg_image'),
    ('^admin/bg_image/edit/(\d+)$',   'cms.views.admin_bg_image_edit'),
    ('^admin/bg_image/delete/(\d+)$', 'cms.views.admin_bg_image_delete'),

    ('^admin/category/$',             'cms.views.admin_category'),
    ('^admin/category/edit/(\d+)$',   'cms.views.admin_category_edit'),
    ('^admin/category/delete/(\d+)$', 'cms.views.admin_category_delete'),

    ('^admin/page/$',                 'cms.views.admin_page'),
    ('^admin/page/edit/(\d+)$',       'cms.views.admin_page_edit'),
    ('^admin/page/delete/(\d+)$',     'cms.views.admin_page_delete'),

)


