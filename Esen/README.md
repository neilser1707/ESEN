#ESEN
Un sistema gestor para facilitar la correcta manipulación de contratos de seguros por parte de los agentes de la Empresa de Seguros Nacionales de Cuba:
>La aplicación actual solo permite el trabajo con contratos de vida individual, sin embargo una vez el sistema supere los días planeados para la prueba inicial, entonces será lanzada una aztualización que gestione el completo abanico de contratos ofrecidos por:
> - ESEN

#### **Tabla de contenido:**
* **Instalación**
* **Uso**
* **Características**
* **Contribución**
* **Licencia**

#### Instalación
>1. Clonar el repositorio: git clone
>2. Crea y activa un entorno virtual, así como instalar las dependencias: pipenv install - pipenv shell
>3. Realiza las migraciones: python manage.py migrate

#### Uso
>1. Inicia el servidor de desarrollo: python manage.py runserver
>2. Abre tu navegador y visita http://localhost:8000

#### Características
>1. El proyecto cuenta con 5 aplicaciones incluida la aplicación principal: esen, agentes, contratos, seguros, tomadores
>2. La mayoría de los endpoints se encuentran protegidos con Json Web Tokens 
>3. La aplicación cuenta con test unitarios a través de APITestCase
>4. Cuenta con autorización y trabajo de roles y permisos

#### Contribución
>1. Puedes hacer un fork del repositorio
>2. Crea una nueva rama para tu contribución
>3. Añade tus cambios y haz commit
>4. Envía tus cambios al repositorio
>5. Abre un pull request en GitHub

#### Licencia
###### Licencia MIT
