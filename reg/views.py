# encoding: utf-8
from django.core.urlresolvers import reverse_lazy
from django.core.mail import send_mail
from reg.models import Candidate,CandidateSuggestion,Address,ShopPreferences
from reg.forms import CandidateForm,AddressForm,ShopPreferencesForm
from xeneric.views import MultiFormView
from django.views.generic.base import TemplateView


class FullCandidateFormView(MultiFormView):
	forms_classes = {'candidate':CandidateForm,'address':AddressForm,
					'prefs':ShopPreferencesForm}
	template_name = 'reg/candidate_create.html'
	success_url = reverse_lazy('reg:success')

	def forms_valid(self, forms):
		candidate = forms['candidate'].save(commit=False)
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
		return super(FullCandidateFormView, self).forms_valid(forms)

class SuccessView(TemplateView):
	template_name = 'reg/success_view.html'