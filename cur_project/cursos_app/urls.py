from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'instructores', views.InstructorViewSet)
router.register(r'categorias', views.CategoriaViewSet)
router.register(r'cursos', views.CursoViewSet)
router.register(r'lecciones', views.LeccionViewSet)
router.register(r'matriculas', views.MatriculaViewSet, basename='matricula')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/buscar/', views.buscar_cursos, name='buscar_cursos'),
]
