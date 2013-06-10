# encoding: utf-8
from django.test import TestCase
from django.core.urlresolvers import reverse
from reg.views import FullCandidateFormView
from reg.models import Candidate,CandidateSuggestion,Address,ShopPreferences
from reg.forms import CandidateForm

class RegViewTests(TestCase):
	def test_FullCandidateFormView(self):
		response = self.client.get(reverse('reg:new'))
		self.assertEqual(response.status_code, 200)
		self.assertIn('candidate',response.context)
		self.assertIn('address',response.context)
		self.assertIn('prefs',response.context)

		# Regular candidate should work normally
		kwargs = dict(city='Niteroi',address_line1='Tapuias 110',cep='24360370',
				footwear=True,surfwear=True,first_name='Alexandre',last_name='Porto',
				email='xvaldetaro@gmail.com',dob='251186',cpf='12108055703',sex='M')

		response = self.client.post(reverse('reg:new'), kwargs)
		self.assertRedirects(response, reverse('reg:success'))
		c1 = Candidate.objects.all().filter(first_name='Alexandre', last_name='Porto')[0]
		a1 = c1.address
		self.assertEqual(a1.city, 'Niteroi')

		# Missing required last_name
		kwargs = dict(city='Niteroi',address_line1='Tapuias 110',cep='24360370',
				footwear=True,surfwear=True,first_name='Alexandre',
				email='xvaldetaro@gmail.com',dob='11/11/1986',
				cpf='12108055703',sex='M')

		response = self.client.post(reverse('reg:new'), kwargs)
		errors = response.context['candidate'].errors
		self.assertIsNot(errors, None)

		#repeated email does not work
		kwargs = dict(city='Niteroi',address_line1='Tapuias 110',cep='24360370',
				footwear=True,surfwear=True,first_name='Alexandre',last_name='Porto',
				email='xvaldetaro@gmail.com',dob='11/11/1986',cpf='12108055703',sex='M')

		response = self.client.post(reverse('reg:new'), kwargs)
		errors = response.context['candidate'].errors
		self.assertIsNot(errors, None)

		# new email works
		kwargs = dict(city='Niteroi',address_line1='Tapuias 110',cep='24360370',
				footwear=True,surfwear=True,first_name='Alexandre',last_name='Porto',
				email='another@gmail.com',dob='22/11/1986',cpf='12108055703',sex='M')

		response = self.client.post(reverse('reg:new'), kwargs)
		self.assertRedirects(response, reverse('reg:success'))
		
		# CPF cleaning
		kwargs = dict(city='Niteroi',address_line1='Tapuias 110',cep='24360370',
				footwear=True,surfwear=True,first_name='Alexandre',last_name='Porto',
				email='another2@gmail.com',dob='11/11/1986',cpf='121.080.557-03',sex='M')

		response = self.client.post(reverse('reg:new'), kwargs)
		self.assertRedirects(response, reverse('reg:success'))
		c1 = Candidate.objects.all().filter(email='another2@gmail.com')[0]
		self.assertEqual(c1.cpf,'12108055703')

		# invalid CPF
		kwargs = dict(city='Niteroi',address_line1='Tapuias 110',cep='24360370',
				footwear=True,surfwear=True,first_name='Alexandre',last_name='Porto',
				email='another3@gmail.com',dob='11/11/1986',cpf='12208055703',sex='M')

		response = self.client.post(reverse('reg:new'), kwargs)
		errors = response.context['candidate'].errors
		self.assertIsNot(errors, None)

		# underage
		kwargs = dict(city='Niteroi',address_line1='Tapuias 110',cep='24360370',
				footwear=True,surfwear=True,first_name='Alexandre',last_name='Porto',
				email='another4@gmail.com',dob='16/11/2005',cpf='12108055703',sex='M')

		response = self.client.post(reverse('reg:new'), kwargs)
		self.assertContains(response, u'O candidato precisa ter no mínimo 18 anos')
		
		# CEP 
		kwargs = dict(city='Niteroi',address_line1='Tapuias 110',cep='24.360-370',
				footwear=True,surfwear=True,first_name='Alexandre',last_name='Porto',
				email='another5@gmail.com',dob='16/11/86',cpf='12108055703',sex='M')

		response = self.client.post(reverse('reg:new'), kwargs)
		self.assertRedirects(response, reverse('reg:success'))
		c1 = Candidate.objects.all().filter(email='another5@gmail.com')[0]
		self.assertEqual(c1.address.cep,'24360370')