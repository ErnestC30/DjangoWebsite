from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from website.models import Content, Media, Post

@receiver(post_save, sender=Media)
@receiver(post_save, sender=Post)
def create_content(sender, instance, created, **kwargs):
    """Creates a Content object corresponding to a newly created Media or Post object."""
    if created:
        try:
            content_type = ContentType.objects.get_for_model(instance)
            author_id = instance.author.id
            content = Content(content_type=content_type,
                            object_id=instance.id,
                            author_id=author_id)
            content.save()
        except:
            print('error')


@receiver(post_delete, sender=Media)
@receiver(post_delete, sender=Post)
def delete_content(sender, instance, **kwargs):
    """Deletes the Content object when the corresponding Media or Post object is deleted."""
    try:
        content = Content.objects.filter(object_id=instance.id).first()
        content.delete()
        print('content deleted')
    except:
        print('error')
