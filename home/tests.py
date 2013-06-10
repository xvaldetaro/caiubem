# encoding: utf-8
from xeneric.testhelper import MessageAssertTestCase
from django.core.urlresolvers import reverse
from home.views import RegView
from home.models import Candidate,Address,ShopPreferences
from home.forms import CandidateForm

class RegViewTests(MessageAssertTestCase):
	def test_RegPostFormView(self):
		valid_mail = "valid_mail@valid.com"

		response = self.client.get(reverse('home:reg'))
		self.assert_message_contains(response,u"Email inexistente, volte a página inicial")
		response = self.client.get("%s?email=%s"%(reverse('home:reg'),"testmail@test.com"))
		self.assert_message_not_contains(response,u"Email inexistente, volte a página inicial")
		self.assertEqual(response.status_code, 200)
		self.assertIn('candidate',response.context)
		self.assertIn('address',response.context)
		self.assertIn('prefs',response.context)

		# Regular candidate should work normally
		kwargs = dict(city='Niteroi',address='Tapuias 110',cep='24360370',
				footwear=True,surfwear=True,first_name='Alexandre',last_name='Porto',
				email=valid_mail,dob='251186',cpf='12108055703',sex='M')

		response = self.client.post(reverse('home:reg'), kwargs)
		self.assertRedirects(response, reverse('home:home'))
		c1 = Candidate.objects.all().filter(first_name='Alexandre', last_name='Porto')[0]
		a1 = c1.address
		self.assertEqual(a1.city, 'Niteroi')

		# Missing required last_name
		kwargs = dict(city='Niteroi',address='Tapuias 110',cep='24360370',
				footwear=True,surfwear=True,first_name='Alexandre',
				email=valid_mail,dob='11/11/1986',
				cpf='12108055703',sex='M')

		response = self.client.post(reverse('home:reg'), kwargs)
		errors = response.context['candidate'].errors
		self.assertIsNot(errors, None)

		#repeated email does not work
		kwargs = dict(city='Niteroi',address='Tapuias 110',cep='24360370',
				footwear=True,surfwear=True,first_name='Alexandre',last_name='Porto',
				email=valid_mail,dob='11/11/1986',cpf='12108055703',sex='M')

		response = self.client.post(reverse('home:reg'), kwargs)
		errors = response.context['candidate'].errors

		# new email works
		kwargs = dict(city='Niteroi',address='Tapuias 110',cep='24360370',
				footwear=True,surfwear=True,first_name='Alexandre',last_name='Porto',
				email='another@gmail.com',dob='22/11/1986',cpf='12108055703',sex='M')

		response = self.client.post(reverse('home:reg'), kwargs)
		self.assertRedirects(response, reverse('home:home'))
		
		# CPF cleaning
		kwargs = dict(city='Niteroi',address='Tapuias 110',cep='24360370',
				footwear=True,surfwear=True,first_name='Alexandre',last_name='Porto',
				email='another2@gmail.com',dob='11/11/1986',cpf='121.080.557-03',sex='M')

		response = self.client.post(reverse('home:reg'), kwargs)
		self.assertRedirects(response, reverse('home:home'))
		c1 = Candidate.objects.all().filter(email='another2@gmail.com')[0]
		self.assertEqual(c1.cpf,'12108055703')

		# invalid CPF
		kwargs = dict(city='Niteroi',address='Tapuias 110',cep='24360370',
				footwear=True,surfwear=True,first_name='Alexandre',last_name='Porto',
				email='another3@gmail.com',dob='11/11/1986',cpf='12208055703',sex='M')

		response = self.client.post(reverse('home:reg'), kwargs)
		errors = response.context['candidate'].errors
		self.assertIsNot(errors, None)

		# underage
		kwargs = dict(city='Niteroi',address='Tapuias 110',cep='24360370',
				footwear=True,surfwear=True,first_name='Alexandre',last_name='Porto',
				email='another4@gmail.com',dob='16/11/2005',cpf='12108055703',sex='M')

		response = self.client.post(reverse('home:reg'), kwargs)
		self.assertContains(response, u'O candidato precisa ter no mínimo 18 anos')
		
		# CEP 
		kwargs = dict(city='Niteroi',address='Tapuias 110',cep='24.360-370',
				footwear=True,surfwear=True,first_name='Alexandre',last_name='Porto',
				email='another5@gmail.com',dob='16/11/86',cpf='12108055703',sex='M')

		response = self.client.post(reverse('home:reg'), kwargs)
		self.assertRedirects(response, reverse('home:home'))
		c1 = Candidate.objects.all().filter(email='another5@gmail.com')[0]
		self.assertEqual(c1.address.cep,'24360370')

		# home:home email verification and redirection
		# correct
		kwargs = dict(email="other_valid@valid.com")
		response = self.client.post(reverse('home:home'), kwargs)
		self.assertRedirects(response, "%s?email=%s" % (reverse('home:reg'), "other_valid@valid.com"))

		#invalid
		kwargs = dict(email='invalid mail')
		response = self.client.post(reverse('home:home'), kwargs)
		self.assert_message_contains(response, u"inválido")

		#repeated
		kwargs = dict(email=valid_mail)
		response = self.client.post(reverse('home:home'), kwargs)
		self.assert_message_contains(response, u"cadastrado")
