
### i. Explicación detallada de la estructura de carpetas y módulos

El proyecto sigue una arquitectura por capas: `routes` → `controllers` → `models/schemas` → `database/utils`.

```text
GastroEje/
├── app/
│   ├── controllers/
│   │   ├── allergens.py
│   │   ├── auth.py
│   │   ├── categories.py
│   │   ├── dishes.py
│   │   ├── establishment.py
│   │   ├── menu.py
│   │   └── users.py
│   ├── models/
│   │   ├── accessibility_features.py
│   │   ├── allergens.py
│   │   ├── categories.py
│   │   ├── dishes.py
│   │   ├── establishments.py
│   │   ├── menus.py
│   │   ├── reservations.py
│   │   ├── reviews.py
│   │   └── user_allergen.py
│   ├── routes/
│   │   ├── accessibility_features.py
│   │   ├── allergens.py
│   │   ├── categories.py
│   │   ├── dishes.py
│   │   ├── establishments.py
│   │   ├── menu.py
│   │   ├── reservas.py
│   │   └── resenas.py
│   ├── schemas/
│   ├── utils/
│   │   ├── hashing.py
│   │   └── jwt.py
│   ├── config.py
│   ├── database.py
│   └── main.py
├── tests/
├── recreate_tables.py
├── migrate_enums.py
├── requirements.txt
└── .env

```






## i. Estructura de carpetas y modulos

La aplicación esta organizada siguiendo una arquitectura por capas y ramas para que el código se mantenga limpio, ordenado y fácil de mantener.

### app/main.py
- Punto de entrada de la API.
- Crea la instancia de FastAPI, configura la aplicación y registra todos los routers que exponen los endpoints.

### app/config.py
- Centraliza la configuración del proyecto.
- Carga variables desde el archivo .env (base de datos, JWT, entorno, etc.) y las expone para el resto de módulos.

### app/database.py
- Encargado de la conexión con la base de datos.
- Configura SQLAlchemy asíncrono, crea el motor, la sesión AsyncSession y proporciona la dependencia get de la DB que usan los endpoints.

### app/models
- Contiene los modelos que representan las tablas de la base de datos.
- Define entidades y relaciones según el diagrama ER.
- Es la capa que mapea directamente la base de datos relacional hacia SQLAlchemy.

### app/schemas
- Define los modelos Pydantic usados para validar datos de entrada y salida.
- Separa claramente la representación externa (API) de los modelos internos de la base de datos.

### app/routes
- Agrupa los routers de FastAPI por recurso de todas las clases de nuestro proyecto 
- Se encarga de las rutas, parámetros, respuestas HTTP y códigos de estado.
- No contiene lógica de negocio: delega todo a los controladores.

### app/controllers
- Implementa las reglas del sistema y la lógica de cada caso de uso.
- Orquesta operaciones con la base de datos usando los modelos y la sesión.
- Nos ayuda en la logica de negocio en GASTROEJE
- Aplica validaciones adicionales y reglas específicas del dominio para nuestras clases

### app/utils
- Contiene funcionalidades técnicas reutilizables, independientes del dominio:
  - Hashing y verificación de contraseñas.
  - Creación y validación de tokens JWT.
  - Funciones auxiliares para autenticación.

### Otros archivos adicionales e importantes 
- tests/: carpeta preparada para pruebas automáticas con pytest.  
- requirements.txt: Lista de dependencias del proyecto.  
- recreate_tables.py:  Script de ayuda para crear/recrear las tablas.  
- migrate_enums.py: Script de apoyo para migraciones de tipos ENUM.  
- .env → Archivo con variables de entorno   
- venv/ → Entorno virtual local de Python.





ii. Instrucciones completas para ejecutar el proyecto en local y iii. Configuración de entorno virtual, instalación de dependencias y uso de requirements.txt




- Crear entorno virtual:
  -python -m venv venv

- Activar entorno virtual:
  -.\venv\Scripts\Activate

- Instalar dependecias de nuestro proyecto
  - pip install -r requirements.txt

- Levantar nuestras API con el UVICORN
  -uvicorn app.main:app --reload


iv. Configuración de la base de datos y variables de entorno (.env)


- DATABASE_URL=postgresql+asyncpg://neondb_owner:npg_ebiuxdL3MQE1@ep-misty-morning-ac5tetol-pooler.sa-east-1.aws.neon.tech/neondb
  -es la cadena que usa SQLAlchemy para conectarse a la BD, Esta variable es leída por config y database para crear el motor y la sesión asincrona.




v. Enlace o ruta para acceder a la documentación de la API


- en /docs se encuentra toca la documentacion visible que crea el (Swagger) alli se pueden ver todos los endpoints disponibles de nuestro prooyecto




vi. Descripción de cómo se aplicaron los principios SOLID


- Single Responsibility 
  El código está dividido por capas:  
  app/routes solo maneja HTTP (paths, status codes),  
  app/controllers contiene la lógica de negocio,  
  app/models mapea la BD con SQLAlchemy y  
  app/schemas valida datos con Pydantic.  
  Utilidades como app/utils/jwt.py y app/utils/hashing.py se encargan exclusivamente de JWT y hashing.

- Open/Closed 
  El sistema permite añadir nuevos recursos (por ejemplo, “Drinks” o “Promociones”) creando nuevos modelos, schemas, controllers y routers, sin modificar lo ya implementado.  
  Muchas extensiones se hacen agregando funciones nuevas como filtros adicionales en dishes o categories sin tocar las existentes.

-  Interface Segregation 
  Cada caso de uso tiene su propio esquema ligero evitando un único DTO gigante.  
  Los routers también están segregados por recurso (usuarios, platos, categorias,reservas, resenas), de forma que cada cliente consume solo lo que necesita.

- Dependency Inversion 
  Los endpoints dependen de abstracciones, no de detalles y llaman a funciones de controlador en lugar de usar SQL directo.  
  La autenticación usa utilidades que se pueden cambiar sin afectar a routers ni controllers.

- Liskov Substitution 
  En este proyecto no se usan jerarquías de herencia complejas; se favorece la composición y la separación por módulos, por lo que LSP no es tan visible como los otros principios.


