# encoding: utf-8
from django.db import models

class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating ``created`` and ``modified`` fields.
    """
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        abstract = True

class Address(TimeStampedModel):
	city = models.CharField(max_length=20, verbose_name=u'cidade')
	address = models.CharField(max_length=100, verbose_name=u'Endereço')
	cep = models.CharField(max_length=10, verbose_name=u'CEP')

	def __unicode__(self):
		return "%s - %s" % (address_line1, city)


class ShopPreferences(TimeStampedModel):
	footwear = models.BooleanField(verbose_name=u'Calçado')
	casualwear = models.BooleanField(verbose_name=u'Roupa casual')
	socialwear = models.BooleanField(verbose_name=u'Roupa social')
	purse = models.BooleanField(verbose_name=u'Bolsa')
	jewelry = models.BooleanField(verbose_name=u'Bijuteria')
	underwear = models.BooleanField(verbose_name=u'Meias e roupas intimas')
	lingerie = models.BooleanField(verbose_name=u'Lingerie')
	jeans = models.BooleanField(verbose_name=u'Jeans')
	surfwear = models.BooleanField(verbose_name=u'Surfwear')

	other = models.TextField(verbose_name=u'Outros a especificar', blank=True)

	def __unicode__(self):
		return unicode(self.candidate)

class Candidate(TimeStampedModel):
	SEX = (('M', 'Masculino'),('F','Feminino'))
	first_name = models.CharField(max_length=15, verbose_name=u'Nome')
	last_name = models.CharField(max_length=25, verbose_name=u'Sobrenome')
	email = models.EmailField(primary_key=True)
	dob = models.DateField(verbose_name=u'Data de nascimento')
	cpf = models.CharField(max_length=14,verbose_name=u'CPF/CNPJ')
	sex = models.CharField(max_length=1, choices=SEX, verbose_name=u'Sexo')

	address = models.ForeignKey(Address)
	preferences = models.OneToOneField(ShopPreferences)

	def __unicode__(self):
		return self.email
