from django.contrib import admin

from base.models import Attendants, Feedbacks, Offers, Profiles, Tags, Profiles

# Register your models here.

admin.site.register(Profiles)
admin.site.register(Offers)
admin.site.register(Tags)
admin.site.register(Feedbacks)
admin.site.register(Attendants)
