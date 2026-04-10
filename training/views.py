

from django.db import connection
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from training.models import Cours, Formateur, Apprenant
from django.contrib.auth.mixins import LoginRequiredMixin , UserPassesTestMixin
from django.contrib import messages
from django.template.context_processors import request
from rest_framework.permissions import IsAuthenticated





# Create your views here.
def home(request):
    return (HttpResponse('<h1> Training Plateforme </h1>'))

from django.views.generic import TemplateView

class AProposView(TemplateView):
    template_name = 'training/a_propos.html'


# def liste_cours(request):
#     cours = Cours.objects.all() # objects.all() retourne une liste des élémént du modèle en question

# # après récupération de la liste des cours, envoyé cette pour affichagee dans un template : liste_cours.html   
#     context ={
#         'cours' : cours
#     }
#     return render(request, 'training/liste_cours.html', context)

class CoursListView(LoginRequiredMixin, ListView):
    model = Cours
    template_name ='training/cours/cours_list.html'
    context_object_name ='cours'
    


# Détails d'un cours

class CoursDetailView(DetailView):
    model= Cours
    template_name = 'training/cours/cours_detail.html'
    context_object_name ='cours'


class CoursCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model= Cours
    template_name = 'training/cours/cours_form.html'
    fields =['titre', 'description', 'duree', 'formateur', 'apprenants']
    success_url = reverse_lazy ('cours_list')
    def test_func(self):
        return self.request.user.groups.filter(name='formateurs').exists()
    def handle_no_permission(self):
        messages.error(self.request, "Accès refusé : Seuls les formateurs peuvent ajouter un cours")
        return redirect('cours_list')

class CoursUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Cours
    template_name = 'training/cours/cours_form.html'
    fields =['titre', 'description', 'duree', 'formateur', 'apprenants']
    success_url = reverse_lazy ('cours_list')
    def test_func(self):
        return self.request.user.groups.filter(name='formateurs').exists()

class CoursDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Cours
    template_name = 'training/cours/cours_confirm_delete.html'
    success_url = reverse_lazy ('cours_list')
    def test_func(self):
        return self.request.user.groups.filter(name='formateurs').exists()

class InscriptionCoursView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        cours = get_object_or_404(Cours, pk=pk)
        
        # Option 2: Find or create Apprenant based on logged-in user's email
        apprenant, created = Apprenant.objects.get_or_create(
            email=request.user.email,
            defaults={'nom': request.user.get_full_name() or request.user.username}
        )
        
        # Toggle enrollment
        if apprenant in cours.apprenants.all():
            cours.apprenants.remove(apprenant)
            messages.info(request, f"Vous vous êtes désinscrit du cours '{cours.titre}'.")
        else:
            cours.apprenants.add(apprenant)
            messages.success(request, f"Félicitations, vous êtes inscrit au cours '{cours.titre}'.")
            
        return redirect('cours_detail', pk=pk)

class MesCoursListView(LoginRequiredMixin, ListView):
    model = Cours
    template_name = 'training/apprenant/mes_cours.html'
    context_object_name = 'cours'

    def get_queryset(self):
        try:
            apprenant = Apprenant.objects.get(email=self.request.user.email)
            return Cours.objects.filter(apprenants=apprenant)
        except Apprenant.DoesNotExist:
            return Cours.objects.none()



# Formateurs

class FormateurListView(LoginRequiredMixin,ListView):
    model = Formateur
    template_name ='training/formateurs/formateur_list.html'
    context_object_name ='formateurs'


# Détails d'un cours

class FormateurDetailView(DetailView):
    model= Formateur
    template_name = 'training/formateurs/formateur_detail.html'
    context_object_name ='formateur'

# Test Injectio SQL

def test_sql(request):
    id = request.GET.get('id')
    # duree = request.Get.get('duree')
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM training_cours WHERE duree >" + id)
        # cursor.execute("SELECT * FROM training_cours WHERE duree>%s" ,  [id])

        result = cursor.fetchall()
    return HttpResponse (result)

import logging
logger = logging.getLogger(__name__)
def test_logging(request):
    user = request.user if request.user.is_authentificated else None 
    if user:
        logger.info(f"{user.username} conencté")
    else:
        logger.warning("Tentative login échouée")

    return HttpResponse("Logging test effectué")


# VIEWSET 
from rest_framework import viewsets , filters
from training.serializers import CoursSerializer, FormateurSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
# from django.filters.rest_framework import DjangoFilterBackend

class CoursViewSet(viewsets.ModelViewSet):
    queryset = Cours.objects.all()
    serializer_class = CoursSerializer
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['titre', 'formateur__nom'] 

class FormateurViewSet(viewsets.ModelViewSet):
    queryset = Formateur.objects.all()
    serializer_class = FormateurSerializer
    permission_classes = [IsAuthenticated]