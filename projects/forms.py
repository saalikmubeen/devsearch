from django.forms import ModelForm, widgets
from .models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'featured_image', 'demo_link', 'source_link', 'tags']
        widgets = {
            "tags" : widgets.CheckboxSelectMultiple()
        }
        
        
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        
        for value in self.fields.values():
            value.widget.attrs.update({'class': 'input'})