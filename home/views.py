# encoding: utf-8
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.contrib import messages
from xeneric.views import MultiFormView
from django.core.urlresolvers import reverse_lazy,reverse
from django.forms import EmailField
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from home.forms import CandidateForm,AddressForm,ShopPreferencesForm
from home.models import Candidate

class PathMixin(object):
	def get_context_data(self, **kwargs):
		kwargs['path'] = self.request.path
		return super(PathMixin, self).get_context_data(**kwargs)

class AboutView(PathMixin, TemplateView):
	template_name = 'home/base.html'

class ContactView(PathMixin, TemplateView):
	template_name = 'home/contact.html'

class RegView(PathMixin, MultiFormView):
	forms_classes = {'candidate':CandidateForm,'address':AddressForm,
					'prefs':ShopPreferencesForm}
	template_name = 'home/reg.html'
	success_url = reverse_lazy('home:home')

	def get_context_data(self, **kwargs):
		email = ''
		if self.request.method == 'GET':
			email = self.request.GET.get('email')
		elif self.request.method == 'POST':
			email = self.request.POST.get('email')

		if email:
			kwargs['email'] = email
		else:
			messages.error(self.request, u"Email inexistente, volte a página inicial")

		return super(RegView, self).get_context_data(**kwargs)

	def forms_valid(self, forms):
		candidate = forms['candidate'].save(commit=False)
		try:
			Candidate.objects.get(email=candidate.email)
		except Candidate.DoesNotExist:
			address = forms['address'].save()
			prefs = forms['prefs'].save()
			address.save()
			prefs.save()
			candidate.address = address
			candidate.preferences = prefs
			candidate.save()
			send_mail(u'Confirmação de cadastro fitdusa', u'Corpo da mensagem.', 
				u'Não Responder <cadastro@dominiodusa123456.com>',
				[candidate.email], fail_silently=False)
			messages.success(self.request, "Você foi cadastrado com sucesso!")
			return super(RegView, self).forms_valid(forms)
		else:
			return super(RegView, self).forms_invalid(forms)

class HomeView(PathMixin, TemplateView):
	template_name = 'home/home.html'

	def post(self,request,*args,**kwargs):
		email = request.POST['email']
		ef = EmailField()
		try:
			ef.clean(email)
			Candidate.objects.get(email=email)
		except Candidate.DoesNotExist:
			url = "%s?email=%s" % (reverse('home:reg'), email)
			return HttpResponseRedirect(url)
		except ValidationError:
			messages.error(self.request, u"Email inválido")
		else:
			messages.info(self.request, u"O email %s já está cadastrado!" % email)

		return super(HomeView, self).get(request,*args,**kwargs)
