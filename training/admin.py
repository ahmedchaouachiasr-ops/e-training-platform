from django.contrib import admin
from .models import Cours, Formateur, Apprenant

def publier_cours(modeladmin, request, queryset):
    queryset.update(published =True)

class CoursAdmin(admin.ModelAdmin):
    list_display = ('titre','published')
    actions = [publier_cours]
    

admin.site.register(Cours, CoursAdmin)
admin.site.register(Formateur)
admin.site.register(Apprenant)