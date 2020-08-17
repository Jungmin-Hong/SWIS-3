from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField(max_length=10000000000000000,null=True, default='')

    head_image = models.ImageField(upload_to='blog/%Y/%m/%d/', blank=True)

    created = models.DateTimeField()

    created = models.DateTimeField(null=True, default='')
    author = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return '{} :: {}'.format(self.title,self.author)

    def get_absolute_url(self):
        return '/blog/{}', format(self.pk)
    
    
