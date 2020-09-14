from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime, date
from ckeditor.fields import RichTextField #rich text editor

class Category(models.Model):
    name = models.CharField(max_length=255)
    ordering = ('name')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        #return reverse('article-detail', args=(str(self.id))) #where to go after post click
        return reverse('home')

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profile/")
    website_url = models.CharField(max_length=255, null=True, blank=True)
    facebook_url = models.CharField(max_length=255, null=True, blank=True)
    twitter_url = models.CharField(max_length=255, null=True, blank=True)
    instagram_url = models.CharField(max_length=255, null=True, blank=True)
    pinterest_url = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return str(self.user)
    
    def get_absolute_url(self):
        #return reverse('article-detail', args=(str(self.id))) #where to go after post click
        return reverse('home')

class Post(models.Model):
    title = models.CharField(max_length=255)
    header_image = models.ImageField(null=True, blank=True, upload_to="images/")
    title_tag = models.CharField(max_length=255) #in title bar, needs a default
    author = models.ForeignKey(User, on_delete=models.CASCADE) #connect author to user and make that a foreign key ..#deletes a user history if account deleted
    body = RichTextField(blank=True, null=True)
    #body = models.TextField()
    post_date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=255, default='coding')
    snippet = models.CharField(max_length=50) #need a default for existing posts, or django wont work
    likes = models.ManyToManyField(User, related_name='blog_posts') #many to many is table to table

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title + ' | ' + str(self.author) #is an object needs to be converted to string

    def get_absolute_url(self):
        #return reverse('article-detail', args=(str(self.id))) #where to go after post click
        return reverse('home')

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self): #to show up in admin more readable
        return '%s - %s' % (self.post.title, self.name)