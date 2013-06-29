# encoding: utf-8
from home.models import Candidate,ShopPreferences,Address
from django.forms import ModelForm,ValidationError
from django.core.validators import EMPTY_VALUES
from django.forms import ValidationError
from django.forms.fields import CharField
from django.utils.translation import ugettext_lazy as _
from datetime import date
import re

def DV_maker(v):
	if v >= 2:
		return 11 - v
	return 0

class BRCPFCNPJField(CharField):
	max_length=18
	"""
	This field validate a CPF number or a CPF string. A CPF number is
	compounded by XXX.XXX.XXX-VD. The two last digits are check digits. 
	If it fails it tries to validate a CNPJ number or a CNPJ string. 
	A CNPJ is compounded by XX.XXX.XXX/XXXX-XX.
	"""
	default_error_messages = {
		'invalid': _("CPF ou CNPJ invalido"),
		'digits_only': _("Esse campo requer apenas digitos"),
		'max_digits': _("Esse campo requer 11 digitos para CPF ou 14 para CNPJ."),
	}

	def validate_CPF(self, value):
		"""
		Value can be either a string in the format XXX.XXX.XXX-XX or an
		11-digit number.
		"""
		if value in EMPTY_VALUES:
			return u''
		if not value.isdigit():
			value = re.sub("[-\.]", "", value)
		orig_value = value[:]
		try:
			int(value)
		except ValueError:
			raise ValidationError(self.error_messages['digits_only'])
		if len(value) != 11:
			raise ValidationError(self.error_messages['max_digits'])
		orig_dv = value[-2:]

		new_1dv = sum([i * int(value[idx]) for idx, i in enumerate(range(10, 1, -1))])
		new_1dv = DV_maker(new_1dv % 11)
		value = value[:-2] + str(new_1dv) + value[-1]
		new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(range(11, 1, -1))])
		new_2dv = DV_maker(new_2dv % 11)
		value = value[:-1] + str(new_2dv)
		if value[-2:] != orig_dv:
			raise ValidationError(self.error_messages['invalid'])

		return orig_value

	def validate_CNPJ(self, value):
		## Try to Validate CNPJ
		"""
		Value can be either a string in the format XX.XXX.XXX/XXXX-XX or a
		group of 14 characters.
		"""
		if value in EMPTY_VALUES:
			return u''
		if not value.isdigit():
			value = re.sub("[-/\.]", "", value)
		orig_value = value[:]
		try:
			int(value)
		except ValueError:
			raise ValidationError(self.error_messages['digits_only'])
		if len(value) != 14:
			raise ValidationError(self.error_messages['max_digits'])
		orig_dv = value[-2:]

		new_1dv = sum([i * int(value[idx]) for idx, i in enumerate(range(5, 1, -1) + range(9, 1, -1))])
		new_1dv = DV_maker(new_1dv % 11)
		value = value[:-2] + str(new_1dv) + value[-1]
		new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(range(6, 1, -1) + range(9, 1, -1))])
		new_2dv = DV_maker(new_2dv % 11)
		value = value[:-1] + str(new_2dv)
		if value[-2:] != orig_dv:
			raise ValidationError(self.error_messages['invalid'])

		return orig_value
	

	def clean(self, value):

		value = super(BRCPFCNPJField, self).clean(value)
		try:
			orig_value = self.validate_CPF(value)
		except ValidationError:
			orig_value = self.validate_CNPJ(value)

		return orig_value

class CandidateForm(ModelForm):
	cpf = BRCPFCNPJField(label="CPF/CNPJ")

	def clean_dob(self):
		dob = self.cleaned_data['dob']
		today = date.today()
		if (dob.year + 18, dob.month, dob.day) > (today.year, today.month, today.day):
			raise ValidationError(u'O candidato precisa ter no mínimo 18 anos')
		return dob

	def __init__(self, *args, **kwargs):
		super(CandidateForm, self).__init__(*args, **kwargs)
		self.fields['dob'].input_formats=['%d/%m/%Y','%d/%m/%y','%d%m%Y','%d%m%y']

	class Meta:
		model = Candidate
		exclude = ('address','preferences')		

class AddressForm(ModelForm):
	def clean_cep(self):
		value = self.cleaned_data['cep']
		if not value.isdigit():
			value = re.sub("[-\.]", "", value)
		if value.isdigit and len(value) == 8:
			return value
	
		raise ValidationError(u'CEP inválido')

	class Meta:
		model = Address

class ShopPreferencesForm(ModelForm):
	class Meta:
		model = ShopPreferences