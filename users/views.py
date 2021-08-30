from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from website.models import Media, Post, Content
from django.contrib.contenttypes.models import ContentType


#Page to create a new account
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now login.')
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})

#Page for users to see all recent uploads, click on post to comment/read comments.
def recent_activity(request):
    return render(request, 'users/recent_activity.html')

#Page for user to view their own account, make changes to name or change picture.
@login_required
def my_profile(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,
                                         request.FILES,
                                         instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been updated.')
            return redirect('my-profile')
        else:
            print('something went wrong')          
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }

        return render(request, 'users/myprofile.html', context)

#Page to view any user's profile.
def view_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    content_list = Content.objects.filter(author_id=user_id)
    context = {'user': user,
               'content_list': content_list}

    return render(request, 'users/profile.html', context)