from django.views.generic.base import TemplateResponseMixin,ContextMixin,View
from django.http import HttpResponseRedirect
from django.utils.encoding import force_text
from django.core.urlresolvers import reverse_lazy

class MultiFormMixin(ContextMixin):
	forms_classes = {}
	success_url = None
	initial = {}

	def get_initial(self):
		"""
		Returns the initial data to use for forms on this view.
		"""
		return self.initial.copy()

	def get_forms_classes(self):
		return self.forms_classes

	def forms_invalid(self, forms):
		return self.render_to_response(self.get_context_data(**forms))

	def forms_valid(self, forms):
		return HttpResponseRedirect(self.get_success_url())

	def get_success_url(self):
		if self.success_url:
			# Forcing possible reverse_lazy evaluation
			url = force_text(self.success_url)
		else:
			raise ImproperlyConfigured(
				"No URL to redirect to. Provide a success_url.")
		return url

	def get_forms(self, forms_classes):
		forms = {}
		forms_kwargs = self.get_forms_kwargs()

		for class_name,form_class in forms_classes.iteritems():
			forms[class_name] = form_class(**forms_kwargs)
		return forms

	def get_forms_kwargs(self):
		kwargs = {'initial': self.get_initial()}
		if self.request.method in ('POST', 'PUT'):
			kwargs.update({
				'data': self.request.POST,
				'files': self.request.FILES,
			})
		return kwargs

class ProcessMultiFormView(View):
	def get(self, request, *args, **kwargs):
		forms_classes = self.get_forms_classes()
		forms = self.get_forms(forms_classes)

		return self.render_to_response(self.get_context_data(**forms))

	def post(self, request, *args, **kwargs):
		forms_classes = self.get_forms_classes()
		forms = self.get_forms(forms_classes)

		for _,form in forms.iteritems():
			if not form.is_valid():
				return self.forms_invalid(forms)

		return self.forms_valid(forms)

	# PUT is a valid HTTP verb for creating (with a known URL) or editing an
	# object, note that browsers only support POST for now.
	def put(self, *args, **kwargs):
		return self.post(*args, **kwargs)

class MultiFormView(TemplateResponseMixin, MultiFormMixin, ProcessMultiFormView):
	"""
		Similar to FormView but for multiple forms
	"""