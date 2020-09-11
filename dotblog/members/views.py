from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic import DetailView, CreateView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm #django form
from django.contrib.auth.views import PasswordChangeView #
from django.urls import reverse_lazy
from .forms import SignUpForm, EditProfileForm, PasswordChangingForm, ProfilePageForm #our form
from theblog.models import Profile

class CreateProfilePageView(CreateView):
    model = Profile
    form_class = ProfilePageForm
    template_name = 'registration/create_user_profile_page.html'
    #fields = '__all__'

    #next code hijacks the form as user is using it.
    def form_valid(self, form): #theres a user filling out the form, lets grab that user. take user id '7'
        form.instance.user = self.request.user #make that user available to the form itself. put it on the form, make form equal to
        return super().form_valid(form) #make sure info gets saved under the correct user. save the form.

class EditProfilePageView(generic.UpdateView):
    model = Profile
    template_name = 'registration/edit_profile_page.html'
    fields = ['bio', 'profile_pic', 'website_url', 'facebook_url', 'twitter_url', 'instagram_url', 'pinterest_url']
    success_url = reverse_lazy('home')

class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'registration/user_profile.html'

    def get_context_data(self, *args, **kwargs): 
        #users = Profile.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)

        page_user = get_object_or_404(Profile, id=self.kwargs['pk']) #pk getting from kwargs, getting from url

        context["page_user"] = page_user
        return context


class PasswordsChangeView(PasswordChangeView): #passwordSSSSS vs password. note!!
    form_class = PasswordChangingForm #the form we show on page
    #form_class = PasswordChangeForm
    success_url = reverse_lazy('password_success')
    #success_url = reverse_lazy('home')

def password_success(request): #create our successful password change view
    return render(request, 'registration/password_success.html', {}) #all it does is send us to this page

class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

class UserEditView(generic.UpdateView):
    form_class = EditProfileForm #our new form
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user