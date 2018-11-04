""" 
Views for Croftair.
"""

from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render

from croftair.models import Subject, Group


class HomeView(TemplateView):
    """ 
    Home page.
    """
    template_name = 'index.html'

class SubjectView(DetailView):
    """ 
    Shows a subject page.
    """
    template_name = 'subject.html'
    model = Subject
    slug_url_kwarg = 'subject_slug'
    
    def get_template_names(self):
        """ 
        Gets a graphic or subject template, depending on the subject type.
        """
        if self.get_object().subject_type == 'graphic':
            return ['graphic.html']
        else:
            return ['subject.html']

class RandomSubjectView(DetailView):
    """ 
    Gets a random subject.
    """
    template_name = 'subject.html'
    model = Subject
    
    def get_object(self):
        """ 
        Gets a random subject.
        """
        return self.get_queryset().all().order_by('?').first()

class TOCView(ListView):
    """ 
    Shows a list of subjects.
    """
    template_name = 'subject_list.html'
    model = Subject


def view_group(request, group_slug):
    """ 
    View to route to a group.
    """
    try:
        group = Group.objects.get(slug=group_slug)
        if group.related_subject:
            return HttpResponseRedirect('/subject/%s/' % group.related_subject.slug)
        else:
            return render(request, 'group.html', context={'group':group})
    except Group.DoesNotExist:
        raise Http404()