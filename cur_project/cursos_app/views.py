from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.db.models import Count, Avg, Q
from .models import Instructor, Categoria, Curso, Leccion, Matricula
from .serializers import (
    InstructorSerializer, CategoriaSerializer, CursoSerializer,
    CursoDetailSerializer, LeccionSerializer, MatriculaSerializer,
    MatriculaCreateSerializer
)


class InstructorViewSet(viewsets.ModelViewSet):
    queryset = Instructor.objects.all()
    serializer_class = InstructorSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def cursos(self, request, pk=None):
        instructor = self.get_object()
        cursos = instructor.curso_set.filter(activo=True)
        serializer = CursoSerializer(cursos, many=True)
        return Response(serializer.data)


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.filter(activa=True)
    serializer_class = CategoriaSerializer
    permission_classes = [AllowAny]


class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.filter(activo=True)
    serializer_class = CursoSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CursoDetailSerializer
        return CursoSerializer

    @action(detail=False, methods=['get'])
    def populares(self, request):
        cursos = self.get_queryset().annotate(
            estudiantes_count=Count('matricula')
        ).order_by('-estudiantes_count')[:10]
        serializer = self.get_serializer(cursos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def por_categoria(self, request):
        categoria_id = request.query_params.get('categoria')
        if categoria_id:
            cursos = self.get_queryset().filter(categoria_id=categoria_id)
            serializer = self.get_serializer(cursos, many=True)
            return Response(serializer.data)
        return Response({'error': 'Parametro categoria requerido'},
                        status=status.HTTP_400_BAD_REQUEST)


class LeccionViewSet(viewsets.ModelViewSet):
    queryset = Leccion.objects.filter(activa=True)
    serializer_class = LeccionSerializer
    permission_classes = [IsAuthenticated]


class MatriculaViewSet(viewsets.ModelViewSet):
    serializer_class = MatriculaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Matricula.objects.filter(estudiante=self.request.user, activa=True)

    def get_serializer_class(self):
        if self.action == 'create':
            return MatriculaCreateSerializer
        return MatriculaSerializer

    @action(detail=True, methods=['post'])
    def actualizar_progreso(self, request, pk=None):
        matricula = self.get_object()
        progreso = request.data.get('progreso')

        if progreso is not None and 0 <= progreso <= 100:
            matricula.progreso = progreso
            if progreso == 100:
                matricula.completado = True
                from django.utils import timezone
                matricula.fecha_completado = timezone.now()
            matricula.save()
            return Response({'mensaje': 'Progreso actualizado'})

        return Response({'error': 'Progreso debe estar entre 0 y 100'},
                        status=status.HTTP_400_BAD_REQUEST)


# ENDPOINT PERSONALIZADO

@api_view(['GET'])
@permission_classes([AllowAny])
def buscar_cursos(request):
    query = request.query_params.get('q', '')
    categoria = request.query_params.get('categoria', '')
    nivel = request.query_params.get('nivel', '')
    precio_max = request.query_params.get('precio_max', '')

    cursos = Curso.objects.filter(activo=True)

    if query:
        cursos = cursos.filter(
            Q(titulo__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(instructor__user__first_name__icontains=query) |
            Q(instructor__user__last_name__icontains=query)
        )

    if categoria:
        cursos = cursos.filter(categoria_id=categoria)

    if nivel:
        cursos = cursos.filter(nivel=nivel)

    if precio_max:
        try:
            cursos = cursos.filter(precio__lte=float(precio_max))
        except ValueError:
            pass

    # ORDENAMOS POR RELEVANCIA, ES DECIR NUMERO DE ESTUDIANTES
    cursos = cursos.annotate(
        estudiantes_count=Count('matricula')
    ).order_by('-estudiantes_count')

    serializer = CursoSerializer(cursos, many=True)
    return Response({
        'total': cursos.count(),
        'cursos': serializer.data
    })
