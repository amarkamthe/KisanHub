from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.template import RequestContext, loader

@staff_member_required
def index(request):
	"""Renders the index template in browser"""
	template = loader.get_template('index.html')
	context = RequestContext(request, {})
	return HttpResponse(template.render(context))
