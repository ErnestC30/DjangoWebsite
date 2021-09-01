from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='web-home'),
    path('upload/', views.upload, name='web-media-upload'),
    path('recent-activity/', views.recent_activity, name='recent-activity'),
    path('post/<int:post_id>', views.view_post, name='view-post'),
    path('post/<int:post_id>/delete', views.delete_comment, name='delete-comment')
]
