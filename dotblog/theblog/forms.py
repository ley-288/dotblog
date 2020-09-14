from django import forms
from .models import Post, Category, Comment

choices = Category.objects.all().values_list('name','name')

choice_list = []

for item in choices:
    choice_list.append(item)

class PostForm(forms.ModelForm): #allows us to create form fields from our model. our Post model.
    class Meta:
        model = Post
        fields = ('title', 'title_tag', 'author', 'category', 'body', 'snippet', 'header_image') #define the fields in our form

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}), #form-control is bootstrap css class
            'title_tag': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'value':'', 'id':'elder', 'type':'hidden'}),
            #'author': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(choices=choice_list, attrs={ 'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'snippet': forms.TextInput(attrs={'class': 'form-control'}),
        }

class EditForm(forms.ModelForm): #edit form instead
    class Meta:
        model = Post
        fields = ('title', 'title_tag', 'body', 'snippet') 

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}), 
            'title_tag': forms.TextInput(attrs={'class': 'form-control'}),
            #'author': forms.Select(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'snippet': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body') 

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}), 
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }