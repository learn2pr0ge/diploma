from django.contrib import admin
from .models import Car, Technicalmaintenance, Claimservice, Booktechnic, Bookengine, Bookclutch, Bookaxle, Bookbridge,Bookcompanies, Booktm, Bookclaimpart, Bookclaimrecover


class CarsAdmin(admin.ModelAdmin):
    model = Car


class TechAdmin(admin.ModelAdmin):
    model = Technicalmaintenance

class ClaimServiceAdmin(admin.ModelAdmin):
    model = Claimservice

class BooktechnicAdmin(admin.ModelAdmin):
    model = Booktechnic

class BookengineAdmin(admin.ModelAdmin):
    model = Bookengine

class BookclutchAdmin(admin.ModelAdmin):
    model = Bookclutch

class BookaxleAdmin(admin.ModelAdmin):
    model = Bookaxle

class BookbridgeAdmin(admin.ModelAdmin):
    model = Bookbridge

class BookcompaniesAdmin(admin.ModelAdmin):
    model = Bookcompanies

class BooktmAdmin(admin.ModelAdmin):
    model = Booktm

class BookclaimpartAdmin(admin.ModelAdmin):
    model = Bookclaimpart

class BookclaimrecoverAdmin(admin.ModelAdmin):
    model = Bookclaimrecover

admin.site.register(Car, CarsAdmin)
admin.site.register(Technicalmaintenance, TechAdmin)
admin.site.register(Claimservice, ClaimServiceAdmin)
admin.site.register(Booktechnic, BooktechnicAdmin)
admin.site.register(Bookengine, BookengineAdmin)
admin.site.register(Bookclutch, BookclutchAdmin)
admin.site.register(Bookaxle, BookaxleAdmin)
admin.site.register(Bookbridge, BookbridgeAdmin)
admin.site.register(Bookcompanies, BookcompaniesAdmin)
admin.site.register(Booktm, BooktmAdmin)
admin.site.register(Bookclaimpart, BookclaimpartAdmin)
admin.site.register(Bookclaimrecover, BookclaimrecoverAdmin)






# Register your models here.
