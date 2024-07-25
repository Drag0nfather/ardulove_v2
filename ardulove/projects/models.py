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


def change_figure_tags(html_code):
    pattern = r'<figure.*?style="(.*?)".*?src="(.*?)".*?</figure>'
    replacement = r'<img style="\1" src="\2">'
    return re.sub(pattern, replacement, html_code)


def move_images_and_update_paths(instance):
    target_directory = os.path.join('media', 'projects', str(instance.id), 'article')
    os.makedirs(target_directory, exist_ok=True)

    image_sources = re.findall(r'<img[^>]+src="([^">]+)"', instance.article)
    replacement_dict = {}

    for src in image_sources:
        media_prefix, path = src[1:6], src[7:]
        dest_path = os.path.join(media_prefix, 'projects', str(instance.id), 'article', path)
        shutil.move(f'./{src}', dest_path)
        replacement_dict[src] = dest_path

    for old_src, new_src in replacement_dict.items():
        instance.article = instance.article.replace(old_src, f'/{new_src}')

    instance.article = change_figure_tags(instance.article)
    instance.save(update_fields=['article'])


@receiver(post_save, sender=Project)
def change_photo_folder(sender, instance, **kwargs):
    post_save.disconnect(change_photo_folder, sender=Project)
    move_images_and_update_paths(instance)
    post_save.connect(change_photo_folder, sender=Project)

@receiver([post_delete], sender=Project)
def delete_photos_folder(sender, instance, **kwargs):
    folder = str(instance.image).rsplit('/', 1)[0]
    if os.path.exists(f'media/{folder}'):
        shutil.rmtree(f'media/{folder}')
