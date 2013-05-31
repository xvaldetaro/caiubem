from django.db import models
from django.contrib.auth.models import User

class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating ``created`` and ``modified`` fields.
    """
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        abstract = True

class Wallet(models.Model):
	user = models.OneToOneField(User)
	points = models.FloatField(default=0)

	def __unicode__(self):
		return u"%s" % (self.user)

class ProductType(TimeStampedModel):
	name = models.CharField(max_length=15)

	def __unicode__(self):
		return u"%s" % (self.name)

class Store(TimeStampedModel):
	name = models.CharField(max_length=30)
	description = models.TextField(blank=True)
	product_types = models.ManyToManyField(ProductType)

	def __unicode__(self):
		return u"%s" % (self.name)

class Product(TimeStampedModel):
	name = models.CharField(max_length=30)
	description = models.TextField(blank=True)
	product_type = models.ForeignKey(ProductType)
	price = models.IntegerField(default=0)
	store = models.ForeignKey(Store)
	stock = models.IntegerField(default=0)

	def __unicode__(self):
		return u"%s" % (self.name)
