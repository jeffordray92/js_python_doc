import logging

from django import template

from projects.models import Project



register = template.Library()
LOGGER = logging.getLogger('projects')

@register.assignment_tag
def display_latest():
    """
    Displays the *five (5)* latest created :py:class:`Projects`, regardless of its type.\n
    Projects displayed are ordered by its ``created`` and ``name`` attributes.
    """
    return Project.objects.all().order_by('-created', 'name')[:5]

@register.assignment_tag
def display_latest_web():
    """
    Displays the *five (5)* latest created *web* :py:class:`Projects`, ordered by its ``created`` and ``name`` attributes.
    """
    return Project.objects.all().filter(project_type=1).order_by('-created', 'name')[:5]

@register.assignment_tag
def display_latest_mobile():
    """
    Displays the *five (5)* latest created *mobile* :py:class:`Projects`, ordered by its ``created`` and ``name`` attributes.
    """
    return Project.objects.all().filter(project_type=2).order_by('-created', 'name')[:5]

@register.filter(name='add_css')
def add_css(field, css):
   return field.as_widget(attrs={"class":css})

class SetVarNode(template.Node):
 
    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value
 
    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value
        return u""
 
def set_var(parser, token):
    # {% set <var_name>  = <var_value> %}
    parts = token.split_contents()
    if len(parts) < 4:
        LOGGER.error("'set' tag must be of the form:  {% set <var_name>  = <var_value> %}")
        raise template.TemplateSyntaxError("'set' tag must be of the form:  {% set <var_name>  = <var_value> %}")
    return SetVarNode(parts[1], parts[3])
 
register.tag('set', set_var)