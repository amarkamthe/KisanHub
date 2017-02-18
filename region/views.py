from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
# from django.http import HttpResponse
# from django.template import RequestContext, loader
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import render
from statistics import *

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
