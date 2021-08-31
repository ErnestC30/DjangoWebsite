from website.models import Media, Post
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse, resolve
from django.db.models.signals import post_save, post_delete
from website.signals import create_content, delete_content
from .forms import MediaForm, PostForm
from django.contrib.auth.decorators import login_required
import json

from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.decorators import parser_classes
from rest_framework.decorators import api_view



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
            post_save.connect(create_content, sender=Media)
            
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
#Note: breaks when not logged in.
@api_view(['GET', 'POST'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
def view_post(request, post_id):

    media = Media.objects.filter(id=post_id).first()
    posts = Post.objects.filter(posted_to_id=post_id)

    #Only update previous page when it came from recent activity or profile page. (i.e. not update on comment post)
    if request.META['HTTP_REFERER'] != request.build_absolute_uri():
        request.session['prev_page'] = request.META['HTTP_REFERER']

    if request.method == "POST":
        data = request.data

        #Delete the entire Media upload.
        if 'type' in data:
            if data['type'] == 'delete_media':
                media = Media.objects.filter(id=data['media_id']).first()
                media.delete()
                post_delete.connect(delete_content, sender=Media)
                return HttpResponse('200')

        else:
            #Posting comment on to page.
            post_form = PostForm(request.POST)
            if post_form.is_valid():
                form = post_form.save(commit=False)
                form.author = request.user.profile
                form.posted_to = media
                form.save()
                post_save.connect(create_content, sender=Post)
                return redirect('view-post', post_id)

    #Default page GET rendering.
    post_form =  PostForm()
    context = {'media': media,
               'posts': posts,
               'post_form': post_form,
               'current_user': request.user,
               'previous_page': request.session.get('prev_page')
               }

    return render(request, 'website/view_post.html', context)

@login_required
def delete_comment(request, post_id):
    #Deleting post comment on an upload.

    comment = Post.objects.filter(id=post_id).first()
    posted_to_id = comment.posted_to_id

    if request.user.id == comment.author_id:
        comment.delete()
        post_delete.connect(delete_content, sender=Post)
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

