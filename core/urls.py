from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('sobre/', views.sobre, name='sobre'),
    path('faculdades/', views.faculdades_list, name='faculdades_list'),
    path('faculdades/<int:faculdade_id>/', views.faculdade_detail, name='faculdade_detail'),
    path('cursos/', views.cursos_list, name='cursos_list'),
    path('cursos/<int:curso_id>/', views.curso_detail, name='curso_detail'),
    path('noticias/', views.noticias_list, name='noticias_list'),
    path('noticias/<slug:slug>/', views.noticia_detail, name='noticia_detail'),
    path('calendario-academico/', views.calendario_academico, name='calendario_academico'),
    path('organigrama/', views.organigrama, name='organigrama'),
]
