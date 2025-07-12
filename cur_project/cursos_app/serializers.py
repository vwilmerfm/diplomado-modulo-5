from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Instructor, Categoria, Curso, Leccion, Matricula


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class InstructorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    nombre_completo = serializers.CharField(source='__str__', read_only=True)

    class Meta:
        model = Instructor
        fields = '__all__'


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class LeccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leccion
        fields = '__all__'


class CursoSerializer(serializers.ModelSerializer):
    instructor = InstructorSerializer(read_only=True)
    categoria = CategoriaSerializer(read_only=True)
    numero_estudiantes = serializers.ReadOnlyField()
    calificacion_promedio = serializers.ReadOnlyField()

    class Meta:
        model = Curso
        fields = '__all__'


class CursoDetailSerializer(serializers.ModelSerializer):
    instructor = InstructorSerializer(read_only=True)
    categoria = CategoriaSerializer(read_only=True)
    lecciones = LeccionSerializer(many=True, read_only=True, source='leccion_set')
    numero_estudiantes = serializers.ReadOnlyField()
    calificacion_promedio = serializers.ReadOnlyField()

    class Meta:
        model = Curso
        fields = '__all__'


class MatriculaSerializer(serializers.ModelSerializer):
    estudiante = UserSerializer(read_only=True)
    curso = CursoSerializer(read_only=True)

    class Meta:
        model = Matricula
        fields = '__all__'


class MatriculaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        fields = ['curso']

    def create(self, validated_data):
        validated_data['estudiante'] = self.context['request'].user
        return super().create(validated_data)
