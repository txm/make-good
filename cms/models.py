from django.db import models

from djangotoolbox.fields import BlobField


class BackgroundImage(models.Model):
    """ BackgroundImage """

    title = models.CharField(max_length=100, help_text='Background image title')
    image = models.FileField(upload_to='bg_images/%Y/%m/%d/%H/%M/%S/')
    #file_name = models.CharField(max_length=1000)
    #content_type = models.CharField(max_length=100)
    blob_key = models.TextField()
    url = models.TextField()
    url_thumb = models.TextField()
    author = models.EmailField(help_text='Your email')
    date_inserted = models.DateField(blank=True, null=True, auto_now_add=1)

    def __unicode__(self):
        return self.title


class About(models.Model):
    """ About """

    name = models.CharField(max_length=100, help_text='Company name')
    email = models.EmailField(help_text='Email')
    telephone = models.CharField(max_length=50, help_text='Telephone')
    address = models.TextField(help_text='Office address')
    blurb = models.TextField(help_text='Some text')

    def __unicode__(self):
        return self.name


class Category(models.Model):
    """ Category """

    name = models.CharField(max_length=100, help_text='Category name')

    def __unicode__(self):
        return self.name


PAGE_TYPES = (
    #('P', 'Portfolio'),
    ('W', 'WYSIWYG'),
    #('G', 'Gallery'),
)


class Page(models.Model):
    """ Page """

    name = models.CharField(max_length=100, help_text='Page name')
    category = models.ForeignKey('Category')
    type = models.CharField(max_length=1, choices=PAGE_TYPES)

    def __unicode__(self):
        return self.name


class PageWYSIWYG(models.Model):
    """ PageWYSIWYG """

    content = models.TextField(help_text='WYSIWYG content')
    page = models.ForeignKey('Page')

    def __unicode__(self):
        return page.name



class Style(models.Model):
    """ Page """

    name = models.CharField(max_length=100, help_text='Style name')
    font_family = models.CharField(max_length=100, help_text='"comma separated", "and double quoted"')

    def __unicode__(self):
        return self.name




