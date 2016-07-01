Reportes  Sermul San Antonio S.C.R.L.
20527478210
SERVICIOS MULTIPLES SAN ANTONIO SOCIEDAD COMERCIAL DE RESPONSABILIDAD LIMITADA

para aplicaciones web seguras escritas en Django y con la el FrontEnd CSS3 Bootstrap.
sermul te permite gestionar las diferentes partes del sistema: usuarios, perfiles,  pagos, libros.
Sermul es la appe web que amigable desarrollado con una metodología scrum desarrollado con python –django  bootstrap- css3
Documentación
Diseño UML
Guía del desarrollador en PDF
Usuario Administrador
Usuario: ruben
Pass: 12345678
Instalación
Para instalar el sermul simplemente lo descargas e instale python 2.7.11 y  los requerimientos de requeriments.txt ejecutando (dentro de la carpeta sermul) el siguiente comando:
backenddj>pip install -r sermul/requirements.txt
Requirements.txt
Django (1.9.7) 
django-db-signals (0.1.1)
django-extensions (1.6.7)
django-formset-js (0.5.0)
django-jquery-js (2.1.4)
django-linguist (0.1.3)
django-registration (2.1.2)
django-rosetta (0.7.11)
microsofttranslator (0.8)
Pillow (3.2.0)
pip (8.1.2)
pkg-resources (0.0.0)
polib (1.0.7)
requests (2.10.0)
setuptools (23.0.0)
six (1.10.0)
wheel (0.29.0)
Local Run
app en forma local el siguiente comando:
backenddj>python manage.py runserver
Usuario: admin
Pass: 12345
Mayor detalle revise 
https://www.youtube.com/watch?v=aUY7fW7z4uI&list=PLEtcGQaT56cg3A3r-TNoc-PyVeOuAMB4x

Detalle de algunas librerías
django-rosetta (0.7.11)	
Con el fin de hacer  un proyecto de Django traducible
Base de datos independiente
Instalado y desinstalado en menos de un minuto
Utiliza la interfaz de administración de Django CSS

línea en el archivo principal urls.py
referencia : https://github.com/mbi/django-rosetta


  

django-db-signals (0.1.1 ) 

Esta aplicación añade un conjunto de señales a algunas de las operaciones de base de datos de Django : django.db.signals.pre_commit django.db.signals.post_commit django.db.signals.pre_rollback django.db.signals.post_rollback django.db.signals.pre_transaction_management django.db.signals.post_transaction_management 

línea en el archivo principal urls.py

referencia: https://github.com/bradleyayers/django-db-signals
  


Template
referencia:  descarga del  link  de abajo  
 https://templated.co/agglomerate
Principales Características
Gestión de Usuarios del sistema.
Permite la creación, edición y eliminación de Usuarios del sistema. Los usuarios del sistema pueden realizar cobros ,  registrar libros y editar sus perfiles usando el modelo en nuestra parte de home
django.contrib.auth.models.User
from django.contrib.auth.models import User
Gestión de Perfiles de usuario.
Permite la creación, edición y eliminación de Perfiles de usuarios.
Gestión de cobros del sistema.
Permite la creación, edición, listado, eliminación de cobros y aumentar servicios del sistema.
Gestión de libros de sistema.
Permite la creación, edición, listado y eliminación de cobros del sistema.
Utilitarios.
sermul es compatible con los navegadores más populares ya que combina HTML5, CSS3 y Javascript. Los idiomas de los mensajes producidos con javascript también pueden extenderse para otro lenguaje en particular.

