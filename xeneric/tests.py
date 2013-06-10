from django.test import TestCase
from xeneric.views import MultiFormView
from django.forms import ModelForm
from django.db import models
from django.http import HttpRequest

class EntityA(models.Model):
	text = models.TextField()
	integer = models.IntegerField()

class EntityB(models.Model):
	text = models.TextField()
	integer = models.IntegerField()

class EntityRel(models.Model):
	text = models.TextField()
	ea = models.ForeignKey(EntityA)
	eb = models.ForeignKey(EntityB)

def create_rel(texta, inta, textb, intb, textr):
	ea = EntityA(text=texta, integer=inta)
	eb = EntityB(text=textb, integer=intb)
	er = EntityRel(text=textr, ea=ea, eb=eb)
	return {'ea':ea,'eb':eb,'er':er}

class ERMTests(TestCase):
	def test_basic_erm(self):
		rel = create_rel('enta',1,'entb',2,'entrel')
		self.assertEqual(rel['er'].eb,rel['eb'])

class EntityAModelForm(ModelForm):
	class Meta:
		model = EntityA

class EntityBModelForm(ModelForm):
	class Meta:
		model = EntityB

class EntityRelModelForm(ModelForm):
	class Meta:
		model = EntityRel

class ERMMultiFormView(MultiFormView):
	forms_classes = {'enta':EntityAModelForm,'entb':EntityBModelForm,
					'entr':EntityRelModelForm}
	template_name = 'dummy'
	success_url = 'dummy'

	def set_request(self, request):
		self.request = request

class XenericTests(TestCase):
	def test_erm_multiformview(self):
		mfv = ERMMultiFormView()
		request = HttpRequest()
		request.method = 'POST'
		request.FILES = {}
		mfv.set_request(request)

		forms_classes = mfv.get_forms_classes()
		self.assertEqual(forms_classes['enta'],EntityAModelForm)
		self.assertEqual(forms_classes['entb'],EntityBModelForm)
		forms = mfv.get_forms(forms_classes)

		entaform = forms['enta']
		self.assertEqual(entaform.is_valid(), False)

		request.POST = {'text':'aaa','integer':2}
		mfv.set_request(request)
		forms = mfv.get_forms(forms_classes)
		self.assertEqual(forms['enta'].is_valid(), True)
		self.assertEqual(forms['entr'].is_valid(), False)