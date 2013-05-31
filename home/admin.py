from django.contrib import admin
from home.models import Candidate,Address,ShopPreferences

class CandidateAdmin(admin.ModelAdmin):
	pass
	
class AddressAdmin(admin.ModelAdmin):
	pass

class ShopPreferencesAdmin(admin.ModelAdmin):
	pass

admin.site.register(Candidate, CandidateAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(ShopPreferences, ShopPreferencesAdmin)