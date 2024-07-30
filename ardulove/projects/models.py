import os.path
import os
import re
import shutil

from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django_ckeditor_5.fields import CKEditor5Field

def project_main_path(instance, filename):
    return f'projects/{instance.id}/{filename}'


class ProjectTag(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Project(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.FileField(upload_to=project_main_path)
    article = CKEditor5Field()
    tags = models.ManyToManyField(ProjectTag, related_name='projects')
    def __str__(self):
        return f'{self.id}: {self.title}'

@receiver([post_save], sender=Project)
def change_photo_folder(sender, instance, **kwargs):
    if kwargs.get('created', None) is False:
        return
    instance_article = instance.article
    image_sources = re.findall(r'<img[^>]+src="([^">]+)"', instance_article)
    replacement_dict = {}
    target_directory = os.path.join('ardulove', 'media', 'projects', str(instance.id), 'article')
    os.makedirs(target_directory, exist_ok=True)
    for ims in image_sources:
        path = ims[ims.rfind('/') + 1:]
        dest_path = os.path.join('ardulove', 'media', 'projects', str(instance.id), 'article', path)
        shutil.move(f'./{ims}', dest_path)
        replacement_dict[ims] = dest_path
    for old_src, new_src in replacement_dict.items():
        instance_article = instance_article.replace(old_src, f'/{new_src}')
    instance.article = instance_article
    instance.save(update_fields=['article'])


@receiver([post_delete], sender=Project)
def delete_photos_folder(sender, instance, **kwargs):
    folder = str(instance.image).rsplit('/', 1)[0]
    if os.path.exists(f'ardulove/media/{folder}'):
        shutil.rmtree(f'ardulove/media/{folder}')
