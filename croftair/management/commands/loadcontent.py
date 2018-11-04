""" 
Loads content into articles.
"""
import os
import os.path

import markdown
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils.text import slugify
from django_static_image import DjangoStaticImageExtension

from croftair.models import Subject, Group, Alias


class Command(BaseCommand):
    """ 
    Command class.
    """
    def handle(self, *args, **kwargs):
        """ 
        Handler method.
        """
        for entry in os.listdir(settings.CONTENT_DIR):
            fullpath = os.path.join(settings.CONTENT_DIR, entry)
            if os.path.isfile(fullpath) and entry.endswith(".md"):
                with open(fullpath) as infile:
                    # extract content and metadata from file
                    md = markdown.Markdown(
                        extensions=["meta", "attr_list", DjangoStaticImageExtension()]
                    )
                    html = md.convert(infile.read())
                    group_names = md.Meta['groups']
                    subject_slug = md.Meta['slug'][0]
                    subject_name = md.Meta['name'][0]
                    alias_names = md.Meta['aliases'] if 'aliases' in md.Meta else []
                    
                    subject_type = md.Meta.get('type', ['subject'])[0]
                    
                    subject = None
                    try:
                        subject = Subject.objects.get(slug=subject_slug)
                        subject.name = subject_name
                        subject.body = html
                        subject.subject_type = subject_type
                        subject.save()
                    except Subject.DoesNotExist:
                        subject = Subject.objects.create(
                            name=subject_name,
                            slug=subject_slug,
                            body=html,
                            subject_type=subject_type,
                        )
                    
                    # If this subject is associated with a group, match it now
                    if Group.objects.filter(name=subject_name).exists():
                        related_group = Group.objects.get(name=subject_name)
                        related_group.related_subject = subject
                        related_group.save()
                    
                    subject.groups.clear()
                    for group_name in group_names:
                        if group_name:
                            group, group_created = Group.objects.get_or_create(name=group_name, slug=slugify(group_name))
                            subject.groups.add(group)
                    
                    subject.save()
                    
                    # Aliases
                    subject.aliases.all().delete()
                    for alias_name in alias_names:
                        if alias_name:
                            Alias.objects.create(subject=subject,
                                                 alias=alias_name)
                    
        
        # get rid of empty groups
        for group in Group.objects.all():
            if group.members.count() == 0:
                if group.related_subject:
                    group.related_subject = None
                    group.save()
                group.delete()
