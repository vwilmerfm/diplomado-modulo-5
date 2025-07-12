from django.contrib import admin

from django.contrib import admin
from .models import Instructor, Categoria, Curso, Leccion, Matricula


# REGISTRAMOS TODOS LOS MODELOS DEFINIDOS

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['user', 'especialidad', 'experiencia_anos', 'activo', 'fecha_registro']
    list_filter = ['especialidad', 'activo', 'experiencia_anos']
    search_fields = ['user__first_name', 'user__last_name', 'especialidad']
    readonly_fields = ['fecha_registro']


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activa']
    list_filter = ['activa']
    search_fields = ['nombre']


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'instructor', 'categoria', 'precio', 'nivel', 'activo', 'numero_estudiantes']
    list_filter = ['categoria', 'nivel', 'activo', 'instructor']
    search_fields = ['titulo', 'descripcion']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion', 'numero_estudiantes', 'calificacion_promedio']
    list_editable = ['precio', 'activo']


@admin.register(Leccion)
class LeccionAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'curso', 'tipo', 'duracion_minutos', 'orden', 'activa']
    list_filter = ['tipo', 'activa', 'curso__categoria']
    search_fields = ['titulo', 'curso__titulo']
    list_editable = ['orden', 'activa']


@admin.register(Matricula)
class MatriculaAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'curso', 'progreso', 'completado', 'calificacion', 'fecha_matricula']
    list_filter = ['completado', 'activa', 'curso__categoria', 'calificacion']
    search_fields = ['estudiante__username', 'curso__titulo']
    readonly_fields = ['fecha_matricula', 'fecha_completado']
    list_editable = ['progreso', 'calificacion']
