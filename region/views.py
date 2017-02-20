from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
# from django.template import RequestContext, loader
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import render
from statistics import *
import json

class IndexView(TemplateView):
	template_name = 'index.html'

	@method_decorator(staff_member_required)
	def get(self, request, *args, **kwargs):
		# Code for GET requests
		return super(IndexView, self).render_to_response({})

	@method_decorator(staff_member_required)
	def post(self, request, *args, **kwargs):
        # Code for POST requests
		context = super(IndexView, self).get_context_data(**kwargs)
		regions = Region.objects.all()
		try:
			for region in regions:
				stat = statistics(region)
				stat.fetch()
			messages.success(request,'Content synced successfully')
		except Exception as e:
			messages.error(request, 'Some error occurred while syncing data ('+str(e)+')')

		return super(IndexView, self).render_to_response(context)

@staff_member_required
def analysis(request, component):
	region = Region.objects.all().values('id','name')
	return render(request, "analysis.html", {'region':region, 'component':component})

@staff_member_required
def rainfall(request, component, region):
	region_data = region_statistical_data(region, component)
	return HttpResponse(json.dumps(region_data), content_type="application/json")

@staff_member_required
def temperature_analysis(request, component):
	region = Region.objects.all().values('id','name')
	return render(request, "temperature_analysis.html", {'region':region, 'component':component})
