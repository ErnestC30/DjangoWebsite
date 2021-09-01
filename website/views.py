from website.models import Media, Post
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models.signals import post_save, post_delete
from website.signals import create_content, delete_content
from .forms import MediaForm, PostForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import InvalidPage, Paginator
from django.http import HttpResponse
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.decorators import parser_classes, api_view

CONTENT_PER_PAGE = 5
DEFAULT_PAGE = 1
PAGE_RANGE = 2

def home(request):
    return render(request, 'website/home.html')

@login_required
def upload(request):
    """Upload an image or video as a Media object to the database.
       Accepts .jpg, .png, .gif for images and .mp4, .webm for videos"""
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

def recent_activity(request):
    """Page for users to see all recent uploads, click on post to comment/read comments."""
    media_list = Media.objects.all().order_by('-id')
    paginator = Paginator(media_list, CONTENT_PER_PAGE)
    page_num = request.GET.get('page', DEFAULT_PAGE)
    try:
        current_page = paginator.page(page_num)
    except InvalidPage:
        current_page = paginator.page(DEFAULT_PAGE)
    page_range = paginator.get_elided_page_range(current_page.number, on_each_side=PAGE_RANGE)

    #Passing the Page object containing a list of Media objects.
    context = {'media_list': current_page,
               'page_range': page_range}
    return render(request, 'website/recent_activity.html', context)

@api_view(['GET', 'POST'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
def view_post(request, post_id):
    """View individual posts, and allow for commenting on post while logged in.
       The user can also view other user's profiles by clicking their names."""
    media = Media.objects.filter(id=post_id).first()
    posts = Post.objects.filter(posted_to_id=post_id)

    #Only update previous page when it came from recent activity or profile page. (i.e. not update on comment post)
    if request.META['HTTP_REFERER'] != request.build_absolute_uri():
        request.session['prev_page'] = request.META['HTTP_REFERER']

    if request.method == "POST":
        data = request.data

        #Deletes the entire Media object when requested.
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
    """Deleting post comment on an upload"""

    comment = Post.objects.filter(id=post_id).first()
    posted_to_id = comment.posted_to_id

    if request.user.id == comment.author_id:
        comment.delete()
        post_delete.connect(delete_content, sender=Post)
        messages.success(request, f'Your comment has been deleted.')
    else:
        messages.warning(request, f'Don\'t delete other\'s comments.')

    return redirect('view-post', posted_to_id)

def getFileType(filename):
    """Determine if uploaded file is an image or video."""
    if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.gif'):
        return 'image'
    elif filename.endswith('.mp4') or filename.endswith('.webm'):
        return 'video'
    else:
        return 'invalid'

