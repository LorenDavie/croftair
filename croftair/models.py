""" 
Models for Croftair site.
"""
from django.db import models
import datetime
from django.template import Template, Context

class Group(models.Model):
    """ 
    A group of subjects.
    """
    name = models.CharField(unique=True, max_length=100)
    slug = models.SlugField()
    related_subject = models.OneToOneField('Subject', related_name='related_group', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.name

subject_types = [
    ('subject', 'subject'),
    ('graphic', 'graphic'),
]

class Subject(models.Model):
    """ 
    An article.
    """
    name = models.CharField(unique=True, max_length=100)
    slug = models.SlugField(unique=True)
    updated = models.DateTimeField(default=datetime.datetime.now)
    groups = models.ManyToManyField(Group, related_name='members')
    body = models.TextField(blank=True)
    subject_type = models.CharField(default='subject', choices=subject_types, max_length=100)
    
    def em_name(self):
        return '<em>%s</em>' % self.name
    
    def render(self):
        """ 
        Renders to get static refs correct.
        """
        text = '{% load static %} ' + self.body
        tmp = Template(text)
        return tmp.render(Context())
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Alias(models.Model):
    """ 
    An alternate name for a subject.
    """
    subject = models.ForeignKey(Subject, related_name='aliases', on_delete=models.CASCADE)
    alias = models.CharField(unique=True, max_length=100)
    
    def em_alias(self):
        return '<em>%s</em>' % self.alias
    
    def __str__(self):
        return self.alias
