from django.contrib import admin
from reg.models import Candidate,Address,ShopPreferences,CandidateSuggestion

class CandidateAdmin(admin.ModelAdmin):
	pass

class CandidateSuggestionAdmin(admin.ModelAdmin):
	pass

class AddressAdmin(admin.ModelAdmin):
	pass

class ShopPreferencesAdmin(admin.ModelAdmin):
	pass

admin.site.register(Candidate, CandidateAdmin)
admin.site.register(CandidateSuggestion, CandidateSuggestionAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(ShopPreferences, ShopPreferencesAdmin)