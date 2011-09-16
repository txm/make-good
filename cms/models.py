from django.db import models

from djangotoolbox.fields import BlobField


class BackgroundImage(models.Model):
    """ BackgroundImage """

    title = models.CharField(max_length=100, help_text='Background image title')
    author = models.EmailField(help_text='Your email')
    image = BlobField(default=None)
    file_name = models.CharField(max_length=1000)
    content_type = models.CharField(max_length=100)
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


class Page(models.Model):
    """ Page """

    PAGE_TYPES = (
        ('P', 'Portfolio'),
        ('T', 'Text'),
    )

    name = models.CharField(max_length=100, help_text='Page name')
    category = models.ForeignKey('Category')
    type = models.CharField(max_length=1, choices=PAGE_TYPES)

    def __unicode__(self):
        return self.name


class Style(models.Model):
    """ Page """

    name = models.CharField(max_length=100, help_text='Style name')

    def __unicode__(self):
        return self.name




