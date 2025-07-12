# Sistema de Cursos

Trabajo final con Django y Django REST Framework. 

### **API REST Completa**
- CRUD completo para todos los modelos
- Autenticacion 
- Paginación automatica
- Busqueda 
- 1 endpoint personalizado

## Tecnologias

- **Backend**: Django 4
- **API**: Django REST 
- **Base de Datos**: SQLite (desarrollo)
- **Autenticacion**: Django Authentication
- **Validacion**: Django Validators
- **CORS**: django-cors-headers
- **Imagenes**: Pillow

## Instalacion

### Prerequisitos
- Python 3.8+
- pip
- virtual env

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/plataforma-cursos.git
cd plataforma-cursos
```

### 2. Crear entorno virtual en Windows
```bash
python -m venv cursosapp-env
cursosapp-env\Scripts\activate

```
### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear superusuario
```bash
python manage.py createsuperuser
```

### 6. Ejecutar servidor
```bash
python manage.py runserver
```

### Para los archivos se crean en la carpeta media, pero es opcional
Los archivos subidos se almacenan en:
- **Imágenes de cursos**: `media/cursos/`
- **Fotos de instructores**: `media/instructores/`
- **Archivos de lecciones**: `media/lecciones/`

## Uso del panel de Admin

### Panel de Administracion
1. Ir a `http://localhost:8000/admin/`
2. Iniciar sesion con el superusuario
3. Crear registros con el Admin en este orden:
   - Categorías
   - Usuarios (instructores/estudiantes)
   - Instructores
   - Cursos
   - Lecciones
   - Matrículas

### API REST
1. **Autenticacion**: `http://localhost:8000/api-auth/login/`
2. **Documentacion**: `http://127.0.0.1:8000/swagger/`
3. **Pruebas**: Usar Postman, Insomnia o el navegador con la documentacion es igual.



### **Endpoint Personalizado (Tambien libres)**

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| `GET` | `/api/buscar/?q=python` | Busqueda avanzada |
| `GET` | `/api/cursos/populares/` | Cursos más populares |
| `GET` | `/api/cursos/por_categoria/?categoria=1` | Filtrar por categoria |
| `POST` | `/api/matriculas/{id}/actualizar_progreso/` | Actualizar progreso |

### 📊 **Ejemplos de Uso**

#### Buscar cursos
```bash
GET /api/buscar/?q=PostgreSQL&categoria=2&nivel=principiante&precio_max=300
```

#### Actualizar progreso de curso
```bash
POST /api/matriculas/1/actualizar_progreso/
{
    "progreso": 75
}
```

## Participante

WILMER FROILAN VILLCA MAMANI

- **Email**: vwilmer.fm@outlook.com
- **GitHub**: [@vwilmerfm](https://github.com/vwilmerfm)


