from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal
import re


class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biografia = models.TextField(max_length=1000)
    especialidad = models.CharField(max_length=100)
    experiencia_anos = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(50)]
    )
    foto = models.ImageField(upload_to='instructores/', blank=True, null=True)
    telefono = models.CharField(max_length=15)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def clean(self):
        # VALIDACION PERSONALIZADA, TELEFONOS QUE EMPEZEN CON 6 o 7, 1ra VALIDACION
        if self.telefono:
            if not re.match(r'^[67]\d{7}$', self.telefono):
                raise ValidationError({
                    'telefono': 'El telefono debe tener 8 dígitos y comenzar con 6 o 7'
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = "Instructor"
        verbose_name_plural = "Instructores"


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(max_length=500)
    icono = models.CharField(max_length=50, blank=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"


class Curso(models.Model):
    NIVELES = [
        ('principiante', 'Principiante'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(max_length=2000)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    nivel = models.CharField(max_length=20, choices=NIVELES)
    duracion_horas = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(500)]
    )
    imagen = models.ImageField(upload_to='cursos/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    requisitos = models.TextField(max_length=1000, blank=True)

    def clean(self):
        # VALIDACON PERSONALIZADA, PRECIO MINIMO, 2DA VALIDACION
        if self.precio and self.precio < Decimal('10.00'):
            raise ValidationError({
                'precio': 'El precio minimo del curso debe ser 10 Bs.'
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def numero_estudiantes(self):
        return self.matricula_set.filter(activa=True).count()

    @property
    def calificacion_promedio(self):
        matriculas = self.matricula_set.filter(activa=True, calificacion__isnull=False)
        if matriculas.exists():
            return matriculas.aggregate(models.Avg('calificacion'))['calificacion__avg']
        return 0

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ['-fecha_creacion']


class Leccion(models.Model):
    TIPOS = [
        ('video', 'Video'),
        ('texto', 'Texto'),
        ('quiz', 'Quiz'),
        ('archivo', 'Archivo'),
    ]

    titulo = models.CharField(max_length=200)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    contenido = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    archivo = models.FileField(upload_to='lecciones/', blank=True, null=True)
    duracion_minutos = models.PositiveIntegerField(default=0)
    orden = models.PositiveIntegerField(default=1)
    gratuita = models.BooleanField(default=False)
    activa = models.BooleanField(default=True)

    def clean(self):
        # VALIDACION PERSONALIZADA, DURACION MINIMA PARA VIDEOS 3RA VALIDACION
        if self.tipo == 'video' and self.duracion_minutos < 1:
            raise ValidationError({
                'duracion_minutos': 'Los videos deben tener al menos 1 minuto de duracion, no puede ser menos..'
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.curso.titulo} - {self.titulo}"

    class Meta:
        verbose_name = "Leccion"
        verbose_name_plural = "Lecciones"
        ordering = ['curso', 'orden']
        unique_together = ['curso', 'orden']


# TANTO EL ISNTRUCTOR Y EL ESTUDIANTE SE CREA DESDE EL ADMIN
class Matricula(models.Model):
    estudiante = models.ForeignKey(User, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_matricula = models.DateTimeField(auto_now_add=True)
    progreso = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    completado = models.BooleanField(default=False)
    fecha_completado = models.DateTimeField(blank=True, null=True)
    calificacion = models.PositiveIntegerField(
        blank=True, null=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comentario = models.TextField(max_length=500, blank=True)
    activa = models.BooleanField(default=True)

    def clean(self):
        # VALIDACION PERSONALIZADA, NO PERMITIR MATRICULAS DUPLICADAS 4TA VALIDACION
        if self.pk is None:  # SE APLICA SOLO PARA LAS NUEVAS MATRICULAS
            if Matricula.objects.filter(
                    estudiante=self.estudiante,
                    curso=self.curso,
                    activa=True
            ).exists():
                raise ValidationError({
                    'curso': 'Ya estas matriculado en este curso'
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.estudiante.username} - {self.curso.titulo}"

    class Meta:
        verbose_name = "Matricula"
        verbose_name_plural = "Matriculas"
        unique_together = ['estudiante', 'curso']
