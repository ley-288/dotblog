from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView ##default django options
from .models import Post, Category, Comment #need to import model to view it
from .forms import PostForm, EditForm, CommentForm ##import form class
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

#def home(request):
 #   return render(request, 'home.html', {})

def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))#get from form and call post id
    liked = False
    if post.likes.filter(id=request.user.id).exists(): #look up if a like has been liked by user id. and if exists..
        post.likes.remove(request.user) #if exists remove it
        liked = False #before liking, liked will be false
    else: #if havent liked..
        post.likes.add(request.user)#adds a like, and from that user
        liked = True #after liking, liked will be true
    return HttpResponseRedirect(reverse('article-detail', args=[str(pk)])) #we want the article detail number, which we get with our args, primary key number

class HomeView(ListView): #all blogs displated. class based view
    model = Post
    template_name = 'home.html'
    #ordering = ['-id'] #latest post first
    ordering = ['-post_date']

    def get_context_data(self, *args, **kwargs): #will add the dropdown menu links to whichever page you want. copy, paste
        cat_menu = Category.objects.all() #everything in our category model. mainly the name and assign to the variable
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context


def CategoryView(request, cats): #function view
    category_posts = Post.objects.filter(category=cats.replace('-', ' ')) #where our categories are sitting, and only display the categories that =cats from our list. 
    return render(request, 'categories.html', {'cats': cats.title().replace('-', ' '), 'category_posts': category_posts})

def CategoryListView(request):
    cat_menu_list = Category.objects.all() #querying category list and passing that variable
    return render(request, 'category_list.html', {'cat_menu_list': cat_menu_list}) #pass into a dictionary which we can now access

class ArticleDetailView(DetailView): #can open a blog and view details
    model = Post
    template_name = 'article_details.html'

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all() #everything in our category model. mainly the name and assign to the variable
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)

        stuff = get_object_or_404(Post, id=self.kwargs['pk'])#look up a post with id of pk.
        total_likes = stuff.total_likes()#function in models.py

        liked = False #set liked to false
        if stuff.likes.filter(id=self.request.user.id).exists(): #lookup post itself by user
            liked = True

        context["cat_menu"] = cat_menu
        context["total_likes"] = total_likes
        context["liked"] = liked #pass into our dictionary
        return context

class AddPostView(CreateView):
    model = Post
    form_class = PostForm #tell to use our form
    template_name = 'add_post.html'
    #fields = '__all__'
    #fields = ('title', 'body')

class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm #tell to use our form
    template_name = 'add_comment.html'
    #fields = '__all__' #dont import fields when you wrote a form that already has fields designated
    def form_valid(self, form): 
        form.instance.post_id = self.kwargs['pk'] 
        return super().form_valid(form) 
    success_url = reverse_lazy('home')
    ordering = ['-datetime_minute']


class AddCategoryView(CreateView):
    model = Category
    #form_class = PostForm #tell to use our form
    template_name = 'add_category.html'
    fields = '__all__'
    #fields = ('title', 'body')

class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'update_post.html'
    #fields = ['title', 'title_tag', 'body']

class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')