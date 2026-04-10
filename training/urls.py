from django.urls import include, path
from training import views
from django.contrib.auth import logout, views as  auth_views
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg  import openapi



router = DefaultRouter()
router.register(r"formateur", views.FormateurViewSet)
router.register(r"cours", views.CoursViewSet)



schema_view = get_schema_view(
    openapi.Info(
        title ="Training Plateforme and API access",
        default_version = "v1",
        description = "Gestion des Cours, Formateurs et des Apprenants",
        ),
        public = True,
        permission_classes= [permissions.AllowAny]
)



urlpatterns = [
    # path('', views.home, name='home'),
    # path('cours/' , views.liste_cours, name="liste_cours")
    path('api/', include(router.urls)),

    path('login/', auth_views.LoginView.as_view(template_name= 'registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name="logout"),

    path('a-propos/', views.AProposView.as_view(), name='a_propos'),

    path('cours/', views.CoursListView.as_view(), name='cours_list'),
    path('cours/<int:pk>', views.CoursDetailView.as_view() , name='cours_detail'),
    path('cours/nouveau/', views.CoursCreateView.as_view(), name = 'cours_create'),
    path('cours/<int:pk>/modifier', views.CoursUpdateView.as_view(), name = 'cours_update'),
    path('cours/<int:pk>/supprimer', views.CoursDeleteView.as_view(), name = 'cours_delete'),
    
    # Apprenant (Etudiant) routes
    path('cours/<int:pk>/inscription/', views.InscriptionCoursView.as_view(), name='cours_inscription'),
    path('mes-cours/', views.MesCoursListView.as_view(), name='mes_cours'),

    # Partie Formateur
    path('formateur/', views.FormateurListView.as_view(), name='formateur_list'),
    path('formateur/<int:pk>', views.FormateurDetailView.as_view() , name='formateur_detail'),
    # test injection sql
    path('test_sql', views.test_sql, name='test_sql'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0)),
    path('redoc', schema_view.with_ui('redoc'), name="redoc")

   

]
