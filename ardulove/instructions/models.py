import os.path
import os
import re
import shutil

from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django_ckeditor_5.fields import CKEditor5Field


def instruction_image_path(instance, filename):
    return f'instructions/{instance.id}/{filename}'


class InstructionTag(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class Instruction(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.FileField(upload_to=instruction_image_path)
    article = CKEditor5Field()
    tags = models.ManyToManyField(InstructionTag, related_name='instructions')
    def __str__(self):
        return f'{self.id}: {self.title}'



def change_figure_tags(html_code):
    pattern = r'<figure.*?style="(.*?)".*?src="(.*?)".*?</figure>'
    replacement = r'<img style="\1" src="\2">'
    return re.sub(pattern, replacement, html_code)


@receiver([post_save], sender=Instruction)
def change_photo_folder(sender, instance, **kwargs):
    # if kwargs.get('created', None) is False:
    #     return
    instance_article = instance.article
    image_sources = re.findall(r'<img[^>]+src="([^">]+)"', instance_article)
    replacement_dict = {}
    target_directory = os.path.join('media', 'instructions', str(instance.id), 'article')
    os.makedirs(target_directory, exist_ok=True)
    for ims in image_sources:
        media_prefix, path = ims[1:6], ims[7:]
        dest_path = os.path.join(media_prefix, 'instructions', str(instance.id), 'article', path)
        shutil.move(f'./{ims}', dest_path)
        replacement_dict[ims] = dest_path
    for old_src, new_src in replacement_dict.items():
        instance_article = instance_article.replace(old_src, f'/{new_src}')
    instance_article = change_figure_tags(instance_article)
    instance.article = instance_article
    post_save.disconnect(change_photo_folder, sender=Instruction)
    instance.save(update_fields=['article'])
    post_save.connect(change_photo_folder, sender=Instruction)


@receiver([post_delete], sender=Instruction)
def delete_photos_folder(sender, instance, **kwargs):
    folder = str(instance.image).rsplit('/', 1)[0]
    if os.path.exists(f'media/{folder}'):
        shutil.rmtree(f'media/{folder}')
