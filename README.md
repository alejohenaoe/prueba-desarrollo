# Prueba de desarrollo - Control de Préstamos de Libros

Esta es una aplicación desarrollada para el control de préstamos de libros en una biblioteca. La aplicación permite a los usuarios registrarse, iniciar sesión, buscar libros por título o autor, prestar libros (lo que actualiza su estado de "disponible" a "no disponible" y asigna una fecha límite de devolución) y devolverlos, restaurando su disponibilidad. Además, se muestra una lista paginada de todos los libros, facilitando la exploración del catálogo.

## Levantamiento de Requerimientos

Para el desarrollo de esta aplicación realicé un análisis de requerimientos que incluyó las siguientes funcionalidades:

- **Registro e Inicio de Sesión:**
  - Como usuario, quiero poder registrarme proporcionando mi nombre, apellido, email y contraseña para tener acceso a la aplicación.
  - Como usuario, quiero iniciar sesión para que la aplicación me reconozca y pueda gestionar mis préstamos.

- **Búsqueda de Libros:**
  - Como usuario, quiero buscar libros por título o autor para encontrar el libro que deseo.
  - La búsqueda debe mostrar la disponibilidad y la opción de préstamo.

- **Préstamo y Devolución de Libros:**
  - Como usuario, quiero poder prestar un libro, lo cual actualizará su estado a "no disponible" y asignará una fecha límite de devolución (una semana).
  - Como usuario, quiero devolver un libro para que su estado vuelva a ser "disponible".

- **Visualización de Libros:**
  - Como usuario, quiero ver los libros que he prestado, junto con la fecha límite para la devolución.
  - Además, quiero ver el catálogo completo de libros paginado (10 libros por página).

## Diseño de Base de Datos

La base de datos fue diseñada usando PostgreSQL y consta de dos tablas principales:

### Tabla `usuario`
- **id:** Identificador único (auto-generado).
- **nombre:** Nombre del usuario.
- **apellido:** Apellido del usuario.
- **email:** Correo electrónico (único).
- **password:** Contraseña encriptada.
- **Relación:** Un usuario puede tener muchos libros prestados.

### Tabla `libro`
- **id:** Identificador único (auto-generado).
- **nombre:** Título del libro.
- **autor:** Autor del libro.
- **fecha_publicacion:** Fecha de publicación.
- **estado:** Estado del libro (puede ser `disponible` o `no disponible`).
- **usuario_id:** Clave foránea que referencia al usuario que tiene el libro en préstamo (nulo si el libro está disponible).
- **fecha_devolucion:** Fecha límite para devolver el libro.

> **Relación:** Es una relación de uno a muchos, ya que un usuario puede tener varios libros prestados, pero cada libro solo se presta a un único usuario.

## Historias de Usuarios

Para garantizar que la aplicación satisficiera las necesidades del usuario, definí las siguientes historias:

1. **Registro de Usuario:**
   - *Como usuario, quiero registrarme en la aplicación para acceder a sus funcionalidades y gestionar mis préstamos.*

2. **Inicio de Sesión:**
   - *Como usuario, quiero iniciar sesión para que la aplicación me identifique y me permita ver mis libros prestados.*

3. **Búsqueda de Libros:**
   - *Como usuario, quiero buscar libros por título o autor para encontrar fácilmente el que necesito.*

4. **Préstamo de Libros:**
   - *Como usuario, quiero prestar un libro para poder leerlo durante una semana y luego devolverlo.*

5. **Devolución de Libros:**
   - *Como usuario, quiero devolver un libro que he prestado para liberar su disponibilidad para otros usuarios.*

6. **Visualización de Catálogo y Préstamos:**
   - *Como usuario, quiero ver una lista paginada de todos los libros y los que tengo prestados junto con la fecha límite de devolución para gestionar mis préstamos.*

## Arquitectura y Tecnologías Utilizadas

- **Backend:** Flask, Flask-SQLAlchemy, Flask-Login.
- **Base de Datos:** PostgreSQL.
- **Frontend:** HTML, CSS y Bootstrap para un diseño moderno y responsivo.
- **Contenerización:** Docker y Docker Compose para el despliegue en contenedores.
- **Control de Versiones:** Git y GitHub.


## Instrucciones de Ejecución

### Ejecución Local

1. Clona el repositorio:
   - git clone https://github.com/alejohenaoe/prueba-desarrollo.git

2. Ingresa al directorio del proyecto:
   - cd prueba-desarrollo

3. Crea el entorno virtual:
   - python -m venv venv

4. Activa el entorno virtual:
   - En Linux/Mac: source venv/bin/activate
   - En Windows: venv\Scripts\activate

5. Instala las dependencias:
   - pip install -r requirements.txt

6. Configura la conexión a la base de datos:
   - En el archivo `app.py` se define la variable `SQLALCHEMY_DATABASE_URI` usando una variable de entorno. Puedes modificarla o exportarla en tu terminal:
     - export SQLALCHEMY_DATABASE_URI=postgresql://usuario:contraseña@localhost:5432/librarydb

7. Ejecuta la aplicación:
   - flask run
     (o, si prefieres usar el intérprete del entorno virtual: python -m flask run)

### Ejecución con Docker

1. Asegúrate de tener Docker y Docker Compose instalados en tu sistema.

2. Desde la raíz del proyecto, ejecuta:
   - docker-compose up --build

3. Accede a la aplicación en el puerto configurado (por ejemplo, http://localhost:5001).

---

## Documentación de app.py

El archivo `app.py` es el corazón de la aplicación y se encarga de:

- Configurar el servidor Flask.
- Conectar a la base de datos PostgreSQL mediante SQLAlchemy.
- Gestionar la autenticación y las sesiones con Flask-Login.
- Definir los modelos de datos y las rutas de la aplicación.

### Modelos

# Diseño de Modelos de la Base de Datos
---

## Modelo `Usuario`

- **id**: Identificador único (clave primaria).
- **nombre**: Nombre del usuario.
- **apellido**: Apellido del usuario.
- **email**: Correo electrónico (único).
- **password**: Contraseña encriptada.

**Relación:**  
Un usuario puede tener muchos libros prestados.

---

## Modelo `Libro`

- **id**: Identificador único (clave primaria).
- **nombre**: Título del libro.
- **autor**: Nombre del autor.
- **fecha_publicacion**: Fecha de publicación del libro.
- **estado**: Estado del libro (puede ser `disponible` o `no disponible`).
- **usuario_id**: Clave foránea que referencia al `id` del Usuario. Es nulo cuando el libro está disponible.
- **fecha_devolucion**: Fecha límite para la devolución del libro.

**Relación:**  
Cada libro, cuando está prestado, se asocia a un único usuario a través del campo `usuario_id`.

---

## Diagrama Entidad-Relación

A continuación se muestra un diagrama entidad-relación utilizando la sintaxis de Mermaid:

```mermaid
erDiagram
    USUARIO {
        int id PK "Primary Key"
        string nombre
        string apellido
        string email
        string password
    }
    LIBRO {
        int id PK "Primary Key"
        string nombre
        string autor
        date fecha_publicacion
        string estado
        int usuario_id FK "Foreign Key (nullable)"
        date fecha_devolucion
    }
    USUARIO ||--o{ LIBRO : "prestado"


