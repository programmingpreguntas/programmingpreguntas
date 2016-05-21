from django import template

register = template.Library()


@register.inclusion_tag('preguntas/vote_buttons.html')
def vote_buttons(votable, request):
    return {'votable_id': votable.id, "votable_type": votable.__class__.__name__, "request": request}
