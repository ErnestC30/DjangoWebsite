from website.models import Media, Post
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import MediaForm, PostForm
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'website/home.html')

@login_required
def upload(request):
    if request.method == "POST":
        media_form = MediaForm(request.POST, 
                               request.FILES)
        if media_form.is_valid():
            #Grabs the submitted form attributes and adds the author property before saving to database.
            form = media_form.save(commit=False)
            filetype = getFileType(form.media.name)
            form.type = filetype
            form.author = request.user
            form.save()
            messages.success(request, f'Your file has been uploaded.')
            return redirect('web-media-upload')
        else:
            #add error here
            print('Something went wrong')

    media_form = MediaForm(instance=request.user)
    context = {'media_form': media_form}
        
    return render(request, 'website/upload.html', context)

#Page for users to see all recent uploads, click on post to comment/read comments.
def recent_activity(request):
    media_list = Media.objects.all()
    context = {'media_list': media_list}
    return render(request, 'website/recent_activity.html', context)

#View individual posts, and allow for commenting on post.
def view_post(request, post_id):

    media = Media.objects.filter(id=post_id).first()
    posts = Post.objects.filter(posted_to_id=post_id)

    if request.method == "POST":
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            form = post_form.save(commit=False)
            form.author = request.user.profile
            form.posted_to = media
            form.save()
            return redirect('view-post', post_id)

    post_form =  PostForm(instance=request.user)
    context = {'media': media,
               'posts': posts,
               'post_form': post_form,
               'current_user': request.user}

    return render(request, 'website/view_post.html', context)

@login_required
def delete_comment(request, post_id):

    comment = Post.objects.filter(id=post_id).first()
    posted_to_id = comment.posted_to_id

    if request.user.id == comment.author_id:
        comment.delete()
        messages.success(request, f'Your comment has been deleted.')
    else:
        messages.warning(request, f'Don\'t delete other\'s comments.')

    return redirect('view-post', posted_to_id)

#Determine if uploaded file is an image or video.
def getFileType(filename):
    if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.gif'):
        return 'image'
    elif filename.endswith('.mp4') or filename.endswith('.webm'):
        return 'video'
    else:
        return 'invalid'