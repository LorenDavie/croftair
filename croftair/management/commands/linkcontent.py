""" 
Links content subjects together.
"""
import re
from django.core.management.base import BaseCommand, CommandError
from croftair.models import Subject

class Command(BaseCommand):
    """ 
    Command class.
    """  
    def handle(self, *args, **kwargs):
        """ 
        Handler method.
        """
        for subject in Subject.objects.all():
            body = subject.body
            
            for inner_subject in Subject.objects.exclude(pk=subject.pk):
                if inner_subject.name in body:
                    print('Detecting', inner_subject.name, 'in body of', subject.name)
                    inner_subject_key = ' %s ' % inner_subject.name
                    
                    inner_subject_em_key = ' <em>%s</em> ' % inner_subject.name
                    inner_subject_replacement = ' <a href="/subject/%s/"><em>%s</em></a> ' % (inner_subject.slug, inner_subject.name)
                    
                    body = body.replace(inner_subject_em_key, inner_subject_replacement)
                    body = body.replace(inner_subject_key, inner_subject_replacement)
                    
                    inner_subject_period_key = ' %s.' % inner_subject.name
                    inner_subject_period_replacement = inner_subject_replacement[:-1] + '.'
                    body = body.replace(inner_subject_period_key, inner_subject_period_replacement)
                    
                    inner_subject_comma_key = ' %s,' % inner_subject.name
                    inner_subject_comma_replacement = inner_subject_replacement[:-1] + ','
                    body = body.replace(inner_subject_comma_key, inner_subject_comma_replacement)
                    
                
                for alias in inner_subject.aliases.all():
                    if alias.alias in body:
                        print('Detecting alias', alias.alias, 'in body of', subject.name)
                        alias_key = ' %s ' % alias.alias
                        alias_em_key = ' <em>%s</em> ' % alias.alias
                        alias_replacement = ' <a href="/subject/%s/"><em>%s</em></a> ' % (inner_subject.slug, alias.alias)
                        
                        body = body.replace(alias_em_key, alias_replacement)
                        body = body.replace(alias_key, alias_replacement)
                        
                        alias_period_key = alias_key[:-1] + '.'
                        alias_period_replacement = alias_replacement[:-1] + '.'
                        body = body.replace(alias_period_key, alias_period_replacement)
                        
                        alias_comma_key = alias_key[:-1] + ','
                        alias_comma_replacement = alias_replacement[:-1] + ','
                        body = body.replace(alias_comma_key, alias_comma_replacement)
            
            subject.body = body
            subject.save()
