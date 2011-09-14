from django.db import models


class Blog(models.Model):
    """ Blog """

    title = models.CharField(max_length=100, help_text='Blog title')
    body = models.TextField(help_text='Blog body')
    author = models.EmailField(help_text='Your email')
    tweeted = models.BooleanField(help_text='Check if you want your post to be tweeted as a tinyurl')
    date = models.DateField(blank=True, null=True, auto_now_add=1)

    def __unicode__(self):
        return self.title

    class Meta:
        app_label = 'make-good'





